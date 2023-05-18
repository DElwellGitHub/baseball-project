import datetime as dt
from statsapi import *

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