from statsapi import *
import datetime as dt
from datetime import datetime
import json
import pathlib
import airflow
import requests
import requests.exceptions as requests_exceptions
import csv
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.amazon.aws.transfers.sql_to_s3 import SqlToS3Operator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from tempfile import NamedTemporaryFile
from airflow.utils.db import provide_session
from airflow.models import XCom

dag = DAG(
    dag_id = "get_todays_gamesv4",
    start_date = dt.datetime(2023, 3, 22),
    #schedule_interval="0 10 * * *",
    schedule_interval=None
    #catchup=True
)


def _call_games(ti,
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

def postgres_to_s3(ds):
    #https://www.youtube.com/watch?v=rcG4WNwi900
    #first query data from psql and save in text file
    hook = PostgresHook(postgres_conn_id="postgres_localhost")
    conn = hook.get_conn()
    cursor = conn.cursor()
    cursor.execute('select * from test_table;')
    with NamedTemporaryFile(mode='w') as f: #puts file in temp folder

    #with open('dags/test_data.txt','w') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow([i[0] for i in cursor.description])
        csv_writer.writerows(cursor)
        f.flush()
        cursor.close()
        conn.close()
        logging.info(f'Ran this on {ds}. Saved postgres data in text file: test_data.txt')
    #step 2: upload text file into s3
        s3_hook = S3Hook(aws_conn_id='aws_hook')
        s3_hook.load_file(
            filename=f.name,
            key=f'games/test_data.txt',
            bucket_name='mlb-project',
            replace=True
        )
        logging.info(f'Test data file {f.name} has been pushed to S3')

print_start = BashOperator(
    task_id="print_start",
    bash_command="echo starting dag",
    dag=dag,
    do_xcom_push=False
)

call_games = PythonOperator(
    task_id="call_games",
    python_callable=_call_games,
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
        create or replace table games_today (
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

sql_to_s3 = PythonOperator(
    dag=dag,
    task_id="postgres_to_s3_task",
    python_callable=postgres_to_s3
)

print_end = BashOperator(
    task_id="print_end",
    bash_command="echo end dag!",
    dag=dag,
    do_xcom_push=False
)
@provide_session
def _delete_xcoms(session=None):
    num_rows_deleted = 0

    try:
        num_rows_deleted = session.query(XCom).delete()
        session.commit()
    except:
        session.rollback()

    print(f"Deleted {num_rows_deleted} XCom rows")

delete_xcoms = PythonOperator(task_id="delete_xcoms", python_callable=_delete_xcoms)

print_start >> call_games >> delete_xcoms
# print_start >> create_sql_table
# call_games >> write_games_sql
# create_sql_table >> write_games_sql
# write_games_sql >> sql_to_s3 >> print_end