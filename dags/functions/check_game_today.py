from airflow.models import XCom
import datetime as dt

def _check_game_today(ti):
    '''
    Check to see if there is or is not a game scheduled today.
    '''
    today_date = dt.datetime.now().strftime('%Y-%m-%d')
    print(today_date)
    games = ti.xcom_pull(key=f'games')
    game_date = next(iter(games.values()))['game_date']
    game_today = 'game_today'
    print_end = 'end_dag'
    try:
        if today_date==game_date:
            print('There is a game today.')
            return game_today
        else:
            print('No game today.')
            return end_dag
    except:
            print('No game today.')
            return end_dag