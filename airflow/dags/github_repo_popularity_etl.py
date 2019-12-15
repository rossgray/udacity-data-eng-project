from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators import (
    StageToRedshiftOperator,
    LoadTableOperator,
    DataQualityOperator,
)
from airflow.operators.dummy_operator import DummyOperator

from helpers import SqlQueries, DataValidationQueries

default_args = {
    'owner': 'rossgray',
    'start_date': datetime(2019, 11, 20),
    'depends_on_past': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    'email_on_retry': False,
}

dag = DAG(
    'github_repo_popularity_etl_v2',
    default_args=default_args,
    description='Full ETL pipeline combining GitHub and Hacker News data',
    schedule_interval=timedelta(days=1),
    catchup=False,
    max_active_runs=1,
)

start_operator = DummyOperator(task_id='Begin_execution', dag=dag)

stage_gh_repos_to_redshift = StageToRedshiftOperator(
    task_id='Stage_gh_repos',
    dag=dag,
    table='staging_github_repos',
    create_table_sql=SqlQueries.create_staging_github_repos,
    s3_key='github_sample.csv',
)

stage_hn_posts_to_redshift = StageToRedshiftOperator(
    task_id='Stage_hn_posts',
    dag=dag,
    table='staging_hacker_news_posts',
    create_table_sql=SqlQueries.create_staging_hacker_news_posts,
    s3_key='hn_sample.csv',
)

load_github_repos_table = LoadTableOperator(
    task_id='Load_github_repos_table',
    dag=dag,
    destination_table='github_repos',
    select_query=SqlQueries.insert_github_repos,
    create_table_sql=SqlQueries.create_github_repos,
)

load_github_users_table = LoadTableOperator(
    task_id='Load_github_users_table',
    dag=dag,
    destination_table='github_users',
    select_query=SqlQueries.insert_github_users,
    create_table_sql=SqlQueries.create_github_users,
)

load_hn_posts = LoadTableOperator(
    task_id='Load_hacker_news_posts',
    dag=dag,
    destination_table='hacker_news_posts',
    select_query=SqlQueries.insert_hacker_news_posts,
    create_table_sql=SqlQueries.create_hacker_news_posts,
)

compute_github_repo_popularity = LoadTableOperator(
    task_id='Compute_github_repo_popularity',
    dag=dag,
    destination_table='github_repo_popularity',
    select_query=SqlQueries.insert_github_repo_popularity,
    create_table_sql=SqlQueries.create_github_repo_popularity,
)

data_validation_github_repos = DataQualityOperator(
    task_id='Data_validation_github_repos',
    dag=dag,
    checks=[
        (DataValidationQueries.data_in_github_repos_table, True),
        (DataValidationQueries.github_repos_owner_null, 0),
        (DataValidationQueries.github_repos_name_null, 0),
        (DataValidationQueries.github_repos_stars_null, 0),
        (DataValidationQueries.github_repos_forks_null, 0),
    ],
)

data_validation_github_users = DataQualityOperator(
    task_id='Data_validation_github_users',
    dag=dag,
    checks=[
        (DataValidationQueries.data_in_github_users_table, True),
        (DataValidationQueries.github_users_name_null, 0),
    ],
)

data_validation_hn_posts = DataQualityOperator(
    task_id='Data_validation_hacker_news_posts',
    dag=dag,
    checks=[
        (DataValidationQueries.data_in_hacker_news_posts_table, True),
        (DataValidationQueries.hn_posts_ref_github_exist, True),
        (DataValidationQueries.hn_posts_points_null, 0),
        (DataValidationQueries.hn_posts_num_comments_null, 0),
    ],
)

data_validation_github_repo_popularity = DataQualityOperator(
    task_id='Data_validation_github_repo_popularity',
    dag=dag,
    checks=[
        (DataValidationQueries.data_in_github_repo_popularity_table, True)
    ],
)

# Define dependencies
# Staging tables
start_operator >> stage_gh_repos_to_redshift
start_operator >> stage_hn_posts_to_redshift

# Dimension tables
stage_gh_repos_to_redshift >> load_github_repos_table
stage_gh_repos_to_redshift >> load_github_users_table

stage_hn_posts_to_redshift >> load_hn_posts

# Data validation
load_github_repos_table >> data_validation_github_repos
load_github_users_table >> data_validation_github_users
load_hn_posts >> data_validation_hn_posts

# Fact table
data_validation_github_repos >> compute_github_repo_popularity
data_validation_github_users >> compute_github_repo_popularity
data_validation_hn_posts >> compute_github_repo_popularity

# Fact table data validation
compute_github_repo_popularity >> data_validation_github_repo_popularity
