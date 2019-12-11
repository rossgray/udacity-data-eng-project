from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults


class DataQualityOperator(BaseOperator):

    ui_color = '#89DA59'

    @apply_defaults
    def __init__(self, checks, redshift_conn_id='redshift', *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.checks = checks

    def execute(self, context):
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)
        for sql, expected_result in self.checks:
            result = redshift.get_first(sql)[0]
            assert (
                result == expected_result
            ), f"""
                Data quality check failed!
                Query: {sql}
                Expected result: {expected_result}
                Actual result: {result}
            """
        self.log.info("All checks passed!")
