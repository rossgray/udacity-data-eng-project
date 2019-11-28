from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators import StageToRedshiftOperator
from airflow.operators.dummy_operator import DummyOperator

from helpers import SqlQueries

default_args = {
    'owner': 'rossgray',
    'start_date': datetime(2019, 11, 20),
    # 'end_date': datetime(2019, 11, 21),
    'depends_on_past': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    'email_on_retry': False,
}

dag = DAG(
    'github_repo_popularity_etl_v3',
    default_args=default_args,
    description='Full ETL pipeline combining GitHub and Hacker News data',
    schedule_interval=timedelta(days=1),
    catchup=False,
)

start_operator = DummyOperator(task_id='Begin_execution', dag=dag)

stage_gh_repos_to_redshift = StageToRedshiftOperator(
    task_id='Stage_gh_repos',
    dag=dag,
    table='staging_github_repos',
    create_table_sql=SqlQueries.create_staging_github_repos,
    s3_key='github_sample.csv',
)

# Define dependencies
start_operator >> stage_gh_repos_to_redshift
