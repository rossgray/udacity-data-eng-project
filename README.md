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
- The `language` and `license` columns for Github repos data are sometimes empty
- To analyse Hacker News activity related to GitHub repos we need to filter rows for which the `URL` contains a GitHub URL (sometimes this `URL` is empty). This is done when loading data from the staging table into the `hacker_news_posts` dimension table using a regular expression.

### Data model



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
