from dags.statsapi import *
import datetime as dt
from datetime import datetime


games = schedule(start_date=dt.datetime.now().strftime('%m/%d/%Y'),
                 end_date=dt.datetime.now().strftime('%m/%d/%Y'))

if __name__=='__main__':
    games = schedule(start_date=dt.datetime.now().strftime('%m/%d/%Y'),
                 end_date=dt.datetime.now().strftime('%m/%d/%Y'))
    print(games)