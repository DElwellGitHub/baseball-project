from dags.statsapi import *
import datetime as dt
from datetime import datetime


games = schedule(start_date=dt.datetime.now().strftime('%m/%d/%Y'),
                 end_date=dt.datetime.now().strftime('%m/%d/%Y'),
                 team=147)

standings = standings_data()

if __name__=='__main__':
    games = schedule(start_date=dt.datetime.now().strftime('%m/%d/%Y'),
                 end_date=dt.datetime.now().strftime('%m/%d/%Y'),
                 team=147)

    # standings = standings_data()
    print(games)
    # for v in standings.values():
    #     #print(v['teams'])
    #     for team in v['teams']:
    #         print(f"{team['name']}, ({team['w']}-{team['l']})")
    #         print(f"{team['name']} are {team['gb']} games back in the division")