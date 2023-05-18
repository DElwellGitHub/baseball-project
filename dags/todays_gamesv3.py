import datetime as dt
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
from airflow.operators.python import BranchPythonOperator
from functions.functions import *
from statsapi import *
from functions import check_game_today


#Instantiate DAG
with DAG(dag_id="get_todays_gamesv3",
         start_date = dt.datetime(2023,4,1), #Start April 1st
         end_date = dt.datetime(2023,10,1), #End October 1st
         schedule_interval="0 15 * * *", #run everyday at 3pm UTC (11am Eastern)
         catchup=False,
         template_searchpath='/airflow-docker/dags/include' #include path to look for external files
        ) as dag:

    print_start = BashOperator(
        task_id="print_start",
        bash_command="echo starting dag",
        dag=dag,
        do_xcom_push=False
    )

    check_game_today = BranchPythonOperator(
        task_id='check_game_today_task',
        python_callable=check_game_today._check_game_today,
        dag=dag
    )

    print_game_today= BashOperator(
        task_id="print_game_today",
        bash_command="echo Game today!",
        dag=dag,
        do_xcom_push=False
    )

    call_games = PythonOperator(
        task_id="call_games",
        python_callable=_call_games,
        dag=dag
    )

    call_standings = PythonOperator(
        task_id="call_standings_task",
        python_callable=_call_standings,
        dag=dag
    )

    scrape_win_prob = PythonOperator(
        task_id = 'scrape_prob_task',
        python_callable = _scrape_prob,
        dag=dag
    )
    
    write_insert_query= PythonOperator(
        task_id = 'write_insert_query_task',
        python_callable= _write_insert_query,
        dag=dag
    )

    create_sql_table = PostgresOperator(
        task_id='create_sql_table_task',
        postgres_conn_id='postgres_localhost',
        sql = 'create_sql_table.sql'
    )

    exec_insert_query = PostgresOperator(
        task_id='exec_insert_query_task',
        postgres_conn_id='postgres_localhost',
        sql ='{{ ti.xcom_pull(key="insert_statements") }}'
    )

    sql_to_s3 = PythonOperator(
        dag=dag,
        task_id="postgres_to_s3_task",
        python_callable=postgres_to_s3
    )

    delete_xcoms = PythonOperator(
        task_id="delete_xcoms", 
        python_callable=_delete_xcoms
    )

    print_end = BashOperator(
        task_id="print_end",
        bash_command="echo end dag!",
        dag=dag,
        do_xcom_push=False
    )

print_start >> call_games >> check_game_today >> [print_game_today, print_end]
print_game_today >> [call_standings, create_sql_table, scrape_win_prob] >> write_insert_query >> exec_insert_query >> [sql_to_s3, delete_xcoms] >>  print_end
