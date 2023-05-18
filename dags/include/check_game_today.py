from airflow.models import XCom

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