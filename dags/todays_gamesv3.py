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


# #Instantiate DAG
# with DAG(dag_id="get_todays_gamesv2",
#          start_date = dt.datetime(2023,4,1), #Start April 1st
#          end_date = dt.datetime(2023,10,1), #End October 1st
#          schedule_interval="0 15 * * *", #run everyday at 3pm UTC (11am Eastern)
#          catchup=False,
#          template_searchpath='/airflow-docker/include' #include path to look for external files
#         ) as dag:

dag = DAG(
    dag_id = "get_todays_gamesv2",
    start_date = dt.datetime(2023,4,1), #Start April 1st
    end_date = dt.datetime(2023,10,1), #End October 1st
    schedule_interval="0 15 * * *", #run everyday at 3pm UTC (11am Eastern)
    catchup=False
)

def _call_games(ti,
                 team=147):
    date_call = dt.datetime.now().strftime('%m/%d/%Y')
    print(date_call)
    games = schedule(start_date=date_call,end_date=date_call,team=team)
    games_dict = {}
    i = 0
    for g in games:
        games_dict[i] = g
        i+=1
    print(games_dict)
    if games_dict[0]['away_probable_pitcher'].strip()=='':
        games_dict[0]['away_probable_pitcher'] = 'TBD'
    if games_dict[0]['home_probable_pitcher'].strip()=='':
        games_dict[0]['home_probable_pitcher'] = 'TBD'
    games_dict[0]['game_time'] = datetimeChange(games_dict[0]['game_datetime']).hr24_to_hr12()
    print(games_dict)
    ti.xcom_push(key=f'games',value=games_dict)

def _call_standings(ti):
    games = ti.xcom_pull(key=f'games')
    print(games)
    for v in games.values():
        home_team = v['home_name']
        away_team = v['away_name']
    standings = standings_data()
    for v in standings.values():
        for team in v['teams']:
            if team['name'] == home_team:
                home_wins = team['w']
                home_losses = team['l']
                if team['gb']=='-':
                    home_gb = 0
                else:
                    home_gb = float(team['gb'])
            if team['name'] == away_team:
                away_wins = team['w']
                away_losses = team['l']
                if team['gb']=='-':
                    away_gb = 0
                else:
                    away_gb = float(team['gb'])
    games['0']['home_wins'] = home_wins
    games['0']['home_losses'] = home_losses
    games['0']['home_gb'] = home_gb
    games['0']['away_wins'] = away_wins
    games['0']['away_losses'] = away_losses
    games['0']['away_gb'] = away_gb
    ti.xcom_push(key='games',value=games)


def _check_game_today(ti,**context):
    today_date = context['execution_date'].strftime('%Y-%m-%d')
    print(today_date)
    games = ti.xcom_pull(key=f'games')
    game_date = next(iter(games.values()))['game_date']
    try:
        if today_date==game_date:
            print('There is a game today.')
            return 'print_game_today'
        else:
            print('No game today.')
            return 'print_end'
    except:
            print('No game today.')
            return 'print_end'   

def _scrape_prob(ti):
    win_prob = scrapeProb('NYY', dt.datetime.now().year).scrape_prob()
    print(f'Win Prob {win_prob}')
    ti.xcom_push(key='win_prob',value=win_prob)


def _write_insert_query(ti,ds):
    games = ti.xcom_pull(key=f'games')
    win_prob = ti.xcom_pull(key='win_prob')
    sql_query = ''
    for k,v in games.items():
        sql_query = sql_query + '\n' + f'''INSERT INTO games (away_name,home_name,away_probable_pitcher,home_probable_pitcher,venue_name,game_date,
                                                              home_wins, home_losses, home_gb, away_wins, away_losses, away_gb, team_win_prob, game_time)
                                   VALUES ('{v['away_name']}','{v['home_name']}','{v['away_probable_pitcher']}',
                                   '{v['home_probable_pitcher']}','{v['venue_name']}','{v['game_date']}',
                                   '{v['home_wins']}','{v['home_losses']}','{v['home_gb']}','{v['away_wins']}','{v['away_losses']}','{v['away_gb']}','{win_prob}','{v['game_time']}');'''
    ti.xcom_push(key=f'insert_statements',value=sql_query)


def postgres_to_s3(ds):
    #https://www.youtube.com/watch?v=rcG4WNwi900
    #first query data from psql and save in text file
    hook = PostgresHook(postgres_conn_id="postgres_localhost")
    conn = hook.get_conn()
    cursor = conn.cursor()
    cursor.execute('select * from games;')
    with NamedTemporaryFile(mode='w') as f: #puts file in temp folder
        csv_writer = csv.writer(f)
        csv_writer.writerow([i[0] for i in cursor.description])
        csv_writer.writerows(cursor)
        f.flush()
        cursor.close()
        conn.close()
        logging.info(f'Ran this on {ds}. Saved postgres data in text file: games.txt')
    #step 2: upload text file into s3
        s3_hook = S3Hook(aws_conn_id='aws_hook')
        s3_hook.load_file(
            filename=f.name,
            key=f'games/games_{ds}.csv',
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

call_standings = PythonOperator(
    task_id="call_standings_task",
    python_callable=_call_standings,
    dag=dag
)

sql_to_s3 = PythonOperator(
    dag=dag,
    task_id="postgres_to_s3_task",
    python_callable=postgres_to_s3
)

print_game_today= BashOperator(
    task_id="print_game_today",
    bash_command="echo Game today!",
    dag=dag,
    do_xcom_push=False
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

create_sql_table = PostgresOperator(
    task_id='create_sql_table_task',
    postgres_conn_id='postgres_localhost',
    sql = '''
        drop table if exists games;
        create table games (
            away_name VARCHAR(40),
            home_name VARCHAR(40),
            away_probable_pitcher VARCHAR(40),
            home_probable_pitcher VARCHAR(40),
            venue_name VARCHAR(40),
            game_date DATE,
            home_wins INT,
            home_losses INT,
            home_gb DECIMAL,
            away_wins INT,
            away_losses INT,
            away_gb DECIMAL,
            team_win_prob VARCHAR(4),
            game_time VARCHAR(9)
            );
    '''
)

write_insert_query= PythonOperator(
    task_id = 'write_insert_query_task',
    python_callable= _write_insert_query,
    dag=dag
)

exec_insert_query = PostgresOperator(
    task_id='exec_insert_query_task',
    postgres_conn_id='postgres_localhost',
    sql ='{{ ti.xcom_pull(key="insert_statements") }}'
)

check_game_today = BranchPythonOperator(
    task_id='check_game_today_task',
    python_callable=_check_game_today,
    dag=dag
)

scrape_win_prob = PythonOperator(
    task_id = 'scrape_prob_task',
    python_callable = _scrape_prob,
    dag=dag
)


print_start >> call_games >> check_game_today >> [print_game_today, print_end]
print_game_today >> [call_standings, create_sql_table] >> write_insert_query >> exec_insert_query >> [sql_to_s3, delete_xcoms] >>  print_end
print_game_today >> scrape_win_prob
