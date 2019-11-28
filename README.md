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

Then visit `localhost:8080` in the browser and enable the example dag in the home page
