import tweepy
import psycopg2
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator

# Set up the Twitter API credentials
consumer_key = 'YOUR_CONSUMER_KEY'
consumer_secret = 'YOUR_CONSUMER_SECRET'
access_token = 'YOUR_ACCESS_TOKEN'
access_token_secret = 'YOUR_ACCESS_TOKEN_SECRET'

# Set up the PostgreSQL database credentials
db_host = 'localhost'
db_port = '5432'
db_name = 'twitter_data'
db_user = 'postgres'
db_password = 'YOUR_DB_PASSWORD'

default_args = {
    'owner': 'Aym0ane',
    'depends_on_past': False,
    'start_date': datetime(2023, 3, 18),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}
dag = DAG('twitter_to_postgres_ETL', default_args=default_args, schedule='@daily')


# Define the tasks
def scrape_twitter_data():
    # Authenticate with Twitter API
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    # Scrape tweets with the hashtag "#example"
    hashtag = '#silicon valley bank'
    tweets = tweepy.Cursor(api.search_tweets, hashtag).items(100)

    # Clean and transform the data
    data = []
    for tweet in tweets:
        tweet_data = {
            'id': tweet.id,
            'created_at': tweet.created_at,
            'text': tweet.text,
            'user_id': tweet.user.id,
            'user_name': tweet.user.name,
            'user_followers': tweet.user.followers_count
        }
        data.append(tweet_data)

    return data

def create_table():
    # Connect to the PostgreSQL database
    conn = psycopg2.connect(host=db_host, port=db_port, dbname=db_name, user=db_user, password=db_password)
    cur = conn.cursor()

    # Create the table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS tweets (
            id BIGINT PRIMARY KEY,
            created_at TIMESTAMP,
            text TEXT,
            user_id BIGINT,
            user_name TEXT,
            user_followers INT
        )
    """)

    # Commit the changes and close the connection
    conn.commit()
    cur.close()
    conn.close()

def load_data():
    # Scrape the data
    data = scrape_twitter_data()

    # Connect to the PostgreSQL database
    conn = psycopg2.connect(host=db_host, port=db_port, dbname=db_name, user=db_user, password=db_password)
    cur = conn.cursor()

    # Insert the data into the table
    for tweet in data:
        cur.execute("""
            INSERT INTO tweets (id, created_at, text, user_id, user_name, user_followers)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (id) DO NOTHING
        """, (tweet['id'], tweet['created_at'], tweet['text'], tweet['user_id'], tweet['user_name'], tweet['user_followers']))

    # Commit the changes and close the connection
    conn.commit()
    cur.close()
    conn.close()


# Define the operators
scrape_data = PythonOperator(
    task_id='scrape_data',
    python_callable=load_data,
    dag=dag
    )
create_table = PythonOperator(
    task_id='create_table',
    python_callable=create_table,
    dag=dag
    )
load_data = PythonOperator(
    task_id='load_data',
    python_callable=load_data,
    dag=dag
    )

# Define the task dependencies
create_table >> scrape_data >> load_data