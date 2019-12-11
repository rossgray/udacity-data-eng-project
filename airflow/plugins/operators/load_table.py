from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults


class LoadTableOperator(BaseOperator):

    ui_color = '#80BD9E'

    sql_template = """
    INSERT INTO {destination_table}
    {select_query}
    ;
    """

    @apply_defaults
    def __init__(
        self,
        destination_table,
        select_query,
        create_table_sql,
        redshift_conn_id='redshift',
        *args,
        **kwargs,
    ):

        super().__init__(*args, **kwargs)
        self.destination_table = destination_table
        self.redshift_conn_id = redshift_conn_id
        self.select_query = select_query
        self.create_table_sql = create_table_sql

    def execute(self, context):
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)

        self.log.info('Creating Redshift table if doesn\'t yet exist')
        redshift.run(self.create_table_sql)

        self.log.info("Clearing data from destination Redshift table")
        redshift.run(f"DELETE FROM {self.destination_table}")

        self.log.info(f"Loading data into {self.destination_table}")
        formatted_sql = self.sql_template.format(
            destination_table=self.destination_table,
            select_query=self.select_query,
        )
        redshift.run(formatted_sql)
