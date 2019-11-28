Udacity Data Engineering Capstone Project
=========================================

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
