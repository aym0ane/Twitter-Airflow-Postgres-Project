
# Twitter Airflow Postgres Project
![profile](https://github.com/aym0ane/Twitter-Airflow-Postgres-Project/blob/main/IMAGES/Twitter%20Airflow%20Postgres%20Project.png)

This project uses Apache Airflow, a popular open-source platform for creating, scheduling, and monitoring workflows. We use Airflow to create an ETL (Extract, Transform, Load) pipeline that scrapes data from Twitter and loads it into a PostgreSQL database. In order to run this pipeline consistently across different environments, we also containerize our Airflow instance using Docker. By doing this, we can ensure that the dependencies and configurations required to run the pipeline are consistent and easily reproducible, regardless of the host environment.


## Table Of Contents
- [Introduction](https://github.com/aym0ane/Twitter-Airflow-Postgres-Project/edit/main/README.md#introduction)
- [Project Architecture](https://github.com/aym0ane/Twitter-Airflow-Postgres-Project/edit/main/README.md#Project-Architecture)
- [Data Extraction](https://github.com/aym0ane/Twitter-Airflow-Postgres-Project/edit/main/README.md#Data-Extraction)
- [Usage](https://github.com/aym0ane/Twitter-Airflow-Postgres-Project/edit/main/README.md#Usage)
- [DAG execution](https://github.com/aym0ane/Twitter-Airflow-Postgres-Project/edit/main/README.md#DAG-execution)
- [PostgreSQL table](https://github.com/aym0ane/Twitter-Airflow-Postgres-Project/edit/main/README.md#PostgreSQL-table)
- [Conclusion](https://github.com/aym0ane/Twitter-Airflow-Postgres-Project/edit/main/README.md#Conclusion)

### Introduction

In this project, we create an ETL (Extract, Transform, Load) pipeline that extracts data from Twitter and loads it into a PostgreSQL database. We use Apache Airflow as our workflow management system to automate the pipeline.

The main goal of this project is to collect tweets related to a particular topic and store them in a database for further analysis. For example, we may be interested in collecting tweets related to a particular product, event, or hashtag.
### Project Architecture

The project architecture consists of the following components:

    Twitter API: We use the Twitter API to access Twitter data. We authenticate with the API using our Twitter developer account credentials.
    Airflow: We use Apache Airflow to schedule and run our ETL pipeline. Airflow is an open-source platform that allows us to create, schedule, and monitor workflows.
    Python: We write Python scripts to implement our data extraction and loading logic. We use the Tweepy library to access the Twitter API, and the Psycopg2 library to interact with the PostgreSQL database.
    PostgreSQL: We use a PostgreSQL database to store our extracted Twitter data. PostgreSQL is a powerful open-source relational database management system.

### Data Extraction

In this project, we use the Twitter API to extract tweets. We first create a Twitter developer account and create an application to obtain our API credentials. We then use the Tweepy library to authenticate with the Twitter API and extract tweets.

We define a Python function that takes a search hashtage as input and uses the Tweepy library to extract tweets related to that hasgtag. We use the tweepy.Cursor object to paginate through the results and extract up to a maximum number of tweets. We then store the extracted tweets in a JSON file.

### Usage
#### Configuring Twitter API and PostgreSQL Credentials
Before running the pipeline, you will need to set up your Twitter API and PostgreSQL credentials in the twitter_to_postgres_ETL.py file. Edit the following lines with your credentials.

#### Running the Pipeline

To run the pipeline, simply trigger the twitter_to_postgres_ETL DAG in the Airflow web interface. This will initiate three tasks:

    create_table: creates a tweets table in the PostgreSQL database if it doesn't already exist.
    scrape_data: scrapes Twitter data with the hashtag "#silicon valley bank" and cleans it.
    load_data: loads the cleaned data into the tweets table in the PostgreSQL database.

You can monitor the progress of each task and view the logs in the Airflow web interface.

![Dag ](https://github.com/aym0ane/Twitter-Airflow-Postgres-Project/blob/main/IMAGES/DAG.JPG)
![Dag map](https://github.com/aym0ane/Twitter-Airflow-Postgres-Project/blob/main/IMAGES/graph.JPG)


### DAG execution
In Airflow, DAGs are scheduled and executed by the Airflow Scheduler based on the specified schedule interval. When a DAG is triggered, the scheduler creates and assigns tasks to workers based on the defined dependencies and execution order. 
if the dag is executed successfuly , we see something like this : 
![dagexecution](https://github.com/aym0ane/Twitter-Airflow-Postgres-Project/blob/main/IMAGES/dag%20execution.JPG)

### PostgreSQL table

As we see we have successfuly load our scraped data to our PostgreSQL database
![postgresTable](https://github.com/aym0ane/Twitter-Airflow-Postgres-Project/blob/main/IMAGES/posstgresql%20table.JPG)

### Conclusion

In this project, we have demonstrated how to create an ETL pipeline to scrape data from Twitter and load it into a PostgreSQL database using Airflow. By using Docker, we can ensure that the pipeline runs consistently and reliably across different environments. This pipeline can be customized to scrape different Twitter data or load it into a different database, making it a flexible and scalable solution for data extraction and processing.
