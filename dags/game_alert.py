import datetime as dt
import airflow
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.operators.python import BranchPythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.operators.dummy_operator import DummyOperator
from functions.statsapi import *
from functions import check_game_today, call_games, call_standings, scrape_prob, write_insert_query, postgres_to_s3, delete_xcoms


#Instantiate DAG
with DAG(dag_id="game_alert",
         start_date = dt.datetime(2023,4,1), #Start April 1st
         end_date = dt.datetime(2023,10,1), #End October 1st
         schedule_interval="0 15 * * *", #run everyday at 3pm UTC (11am Eastern)
         catchup=False,
        ) as dag:

    start_dag = DummyOperator(
        task_id="start_dag",
        dag=dag
    )

    check_game_today = BranchPythonOperator(
        task_id='check_game_today_task',
        python_callable=check_game_today._check_game_today,
        dag=dag
    )

    game_today= DummyOperator(
        task_id="game_today",
        dag=dag
    )

    call_games = PythonOperator(
        task_id="call_games_task",
        python_callable=call_games._call_games,
        op_kwargs = {'team':147}, #Yankees team ID
        dag=dag
    )

    call_standings = PythonOperator(
        task_id="call_standings_task",
        python_callable=call_standings._call_standings,
        dag=dag
    )

    scrape_win_prob = PythonOperator(
        task_id = 'scrape_prob_task',
        python_callable = scrape_prob._scrape_prob,
        op_kwargs = {'short_team_name':'NYY',
                     'long_team_name':'Yankees'}, 
        dag=dag
    )
    
    write_insert_query= PythonOperator(
        task_id = 'write_insert_query_task',
        python_callable= write_insert_query._write_insert_query,
        dag=dag
    )

    create_sql_table = PostgresOperator(
        task_id='create_sql_table_task',
        postgres_conn_id='postgres_localhost',
        sql = '/include/create_table.sql'
    )

    exec_insert_query = PostgresOperator(
        task_id='exec_insert_query_task',
        postgres_conn_id='postgres_localhost',
        sql ='{{ ti.xcom_pull(key="insert_statements") }}'
    )

    postgres_to_s3 = PythonOperator(
        dag=dag,
        task_id="postgres_to_s3_task",
        python_callable=postgres_to_s3._postgres_to_s3
    )

    delete_xcoms = PythonOperator(
        task_id="delete_xcoms", 
        python_callable=delete_xcoms._delete_xcoms
    )

    end_dag = DummyOperator(
        task_id="end_dag",
        dag=dag
    )

#Set up dag dependencies
start_dag >> call_games >> check_game_today >> [game_today, end_dag]
game_today >> [call_standings, create_sql_table, scrape_win_prob] >> write_insert_query >> exec_insert_query >> [postgres_to_s3, delete_xcoms] >>  end_dag

