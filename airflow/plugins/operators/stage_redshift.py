from airflow.contrib.hooks.aws_hook import AwsHook
from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults


class StageToRedshiftOperator(BaseOperator):
    ui_color = '#358140'
    region = 'eu-west-2'
    template_fields = ('s3_key',)
    copy_sql = """
        COPY {}
        FROM '{}'
        ACCESS_KEY_ID '{}'
        SECRET_ACCESS_KEY '{}'
        REGION '{}'
        CSV
        IGNOREHEADER 1
        TIMEFORMAT 'auto'
        ;
    """

    @apply_defaults
    def __init__(
        self,
        table,
        create_table_sql,
        s3_key,
        aws_credentials_id='aws_credentials',
        s3_bucket='udacity-data-eng-project',
        redshift_conn_id='redshift',
        *args,
        **kwargs,
    ):

        super().__init__(*args, **kwargs)
        self.table = table
        self.create_table_sql = create_table_sql
        self.redshift_conn_id = redshift_conn_id
        self.s3_key = s3_key
        self.aws_credentials_id = aws_credentials_id
        self.s3_bucket = s3_bucket

    def execute(self, context):
        aws_hook = AwsHook(self.aws_credentials_id)
        credentials = aws_hook.get_credentials()
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)

        self.log.info('Creating Redshift table if doesn\'t yet exist')
        redshift.run(self.create_table_sql)

        self.log.info('Clearing data from destination Redshift table')
        redshift.run(f'DELETE FROM {self.table}')

        self.log.info('Copying data from S3 to Redshift')
        rendered_key = self.s3_key.format(**context)
        s3_path = 's3://{}/{}'.format(self.s3_bucket, rendered_key)
        formatted_sql = self.copy_sql.format(
            self.table,
            s3_path,
            credentials.access_key,
            credentials.secret_key,
            self.region,
        )
        redshift.run(formatted_sql)
