Udacity Data Engineering Capstone Project
=========================================

Project description
-------------------

The aim for this project is to pull in data from 2 different data sources:

1. List of GitHub repositories created between 29 Oct 2007 and 12 Nov 2010 - [https://www.kaggle.com/qopuir/github-repositories](https://www.kaggle.com/qopuir/github-repositories)
2. Hacker News posts (all posts since 2006) - [https://www.kaggle.com/santiagobasulto/all-hacker-news-posts-stories-askshow-hn-polls](https://www.kaggle.com/santiagobasulto/all-hacker-news-posts-stories-askshow-hn-polls)

This data will then be prepared for analysis to answer questions such as:
- Which Github repos are the most popular according to Hacker News activity?
- Which Github users are generating the most activity on Hacker News?
- Which languages are most popular?

### Data assessment

- The GitHub repo data is just for repos created between certain dates so I decided to limit the date range for which we pull in Hacker News data. There may be some established projects which are still receiving a lot of activity many years after they were created but for efficiency I decided to to limit the Hacker News posts to all posts before 2014.
- The `language`, `license`, `size`, `stars`, `forks`, `open_issues` and `created_at` columns for Github repos data are sometimes empty
- The `num_comments` column for Hacker News posts can sometimes be empty
- To analyse Hacker News activity related to GitHub repos we need to filter rows for which the `URL` contains a GitHub URL (sometimes this `URL` is empty). This is done when loading data from the staging table into the `hacker_news_posts` dimension table using a regular expression.
- Some of the Hacker News URLs are very long, hence the maximum field length for this column has been set to 8192.

### Data model

![Data model](ERDiagram.png)

The above Entity-Relationship Diagram shows the data model used. The two staging tables are on the left and represent the data from the source CSV files with some data types applied to them. The tables on the right represent the dimension tables and the fact table (`github_repo_popularity`). The fact table contains metrics of popularity for GitHub repositories and is designed to help answer the questions posed above.

### ETL pipeline

The ETL (extract-transform-load) pipeline is ran via an Airflow DAG:

![DAG](DAG.png)

The DAG is comprised of a few main stages:
1. We first pull in the data from the two CSV files into two staging tables; one for the GitHub repo data and one for the Hacker News posts.
2. Data is then loaded into the three dimension tables; GitHub repos, GitHub users, and Hacker News posts
3. Data quality checks are then performed on the data to ensure we have data in these tables and that we don't have any values that we're not expecting.
4. The fact table, `github_repo_popularity`, is then built by joining data from two of the dimension tables.
5. A final data validation check is performed on the fact table to ensure we have data.


## Improvements that could be made / next steps

At the moment this data is just a couple of standalone CSV files. We could pull in this data using the GitHub and Hacker News APIs instead so that we get up-to-date data. Using Airflow schedules we could also pull in a subset of data for the time range given by the schedule.




Development
-----------

### Running project for first time

```bash
# Set airflow home directory
export AIRFLOW_HOME=$(pwd)/airflow
```

```bash
# Install requirements
pip install -r requirements.txt
```

```bash
# initialize the database
airflow initdb
```

```bash
# start the web server, default port is 8080
airflow webserver -p 8080
```

```bash
# start the scheduler
airflow scheduler
```

#### Add connection details via Airflow UI
AWS credentials:

Conn Id: Enter `aws_credentials`.
Conn Type: Enter `Amazon Web Services`.
Login: Enter your Access key ID
Password: Enter your Secret access key

Redshift connection details:

Conn Id: Enter `redshift`.
Conn Type: Enter `Postgres`.
Host: Enter the endpoint of your Redshift cluster, excluding the port at the end.
Schema: This is the Redshift database you want to connect to.
Login: Enter Redshift user
Password: Enter Redshift password
Port: Enter 5439.


Then visit `localhost:8080` in the browser and enable the example dag in the home page
