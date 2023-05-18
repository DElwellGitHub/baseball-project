from functions import functions

def _scrape_prob(ti):
    win_prob = scrapeProb('NYY', dt.datetime.now().year).scrape_prob()
    print(f'Win Prob {win_prob}')
    ti.xcom_push(key='win_prob',value=win_prob)