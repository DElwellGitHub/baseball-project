from airflow.models import XCom
from functions.statsapi import standings_data

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