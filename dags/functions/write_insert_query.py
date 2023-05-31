from airflow.models import XCom
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.amazon.aws.transfers.sql_to_s3 import SqlToS3Operator
from airflow.providers.postgres.hooks.postgres import PostgresHook

def _write_insert_query(ti,ds):
    '''
    Write the query that will insert data into Postgres database.
    '''
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