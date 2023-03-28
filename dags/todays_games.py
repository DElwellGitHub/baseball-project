from statsapi import *
import datetime as dt
from datetime import datetime
import json
import pathlib
import airflow
import requests
import requests.exceptions as requests_exceptions
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator

dag = DAG(
    dag_id = "get_todays_gamesv4",
    start_date = dt.datetime(2023, 3, 22),
    #schedule_interval="0 10 * * *",
    schedule_interval=None
    #catchup=True
)


def todays_games(ti,
                 start_date=dt.datetime.now().strftime('%m/%d/%Y'),
                 end_date=dt.datetime.now().strftime('%m/%d/%Y')):
    games = schedule(start_date=start_date,end_date=end_date)
    games_dict = {}
    i = 0
    for g in games:
        games_dict[i] = g
        i+=1
    ti.xcom_push(key=f'games',value=games_dict)

def write_games(ti):
    games_data = ti.xcom_pull(key='games')
    for k,v in games_data.items():
        print(v)

print_start = BashOperator(
    task_id="print_start",
    bash_command="echo starting",
    dag=dag,
    do_xcom_push=False
)

call_games = PythonOperator(
    task_id="call_games",
    python_callable=todays_games,
    dag=dag
)

write_games_s3 = PythonOperator(
    task_id = "write_games_s3",
    python_callable = write_games,
    dag=dag
)

test_postgres1 = PostgresOperator(
    task_id='create_postgres_table',
    postgres_conn_id='postgres_localhost',
    sql = '''
        create table if not exists test_table (
            colA varchar(2),
            colB int,
            colC decimal
        );
    '''

)

test_postgres2 = PostgresOperator(
    task_id='insert1',
    postgres_conn_id='postgres_localhost',
    sql = '''
        insert into test_table
        values ('AB', 9, 3.2);
        
    '''
)

test_postgres3 = PostgresOperator(
    task_id='insert2',
    postgres_conn_id='postgres_localhost',
    sql = '''
        insert into test_table
        values ('XY', 2, 2.1);
    '''
)

test_postgres4 = PostgresOperator(
    task_id='read',
    postgres_conn_id='postgres_localhost',
    sql = '''
        select colA,colB from test_table;
    '''
)

print_end = BashOperator(
    task_id="print_end",
    bash_command="echo end!",
    dag=dag,
    do_xcom_push=False
)

print_start >> call_games >> write_games_s3  >> print_end
print_start >> test_postgres1 >> test_postgres2 >> test_postgres3 >> test_postgres4 >> print_end