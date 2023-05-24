import datetime as dt
from bs4 import BeautifulSoup
import requests
#from functions.functions import scrapeProb


class scrapeProb:
    '''
    Scrape probability that MLB team will win their game.
    '''

    def __init__(self, short_team_name, year):
        self.short_team_name = short_team_name
        self.year = year

    def scrape_prob(self):
        url = f'https://projects.fivethirtyeight.com/{self.year}-mlb-predictions/games/'
        page = requests.get(url)

        soup = BeautifulSoup(page.content, 'html.parser')   
        results_team = soup.find_all('span',class_='team-name short')
        results_win_prob = soup.find('main',class_='container').find('table',class_='table').find_all('td', class_="td number td-number win-prob")

        team_i=0
        for team in results_team:
            if team.get_text()== self.short_team_name:
                team_pct_i=team_i
                break
            team_i+=1

        prob_win = results_win_prob[team_pct_i].get_text()

        return prob_win



def _scrape_prob(ti,short_team_name):
    win_prob = scrapeProb(short_team_name, dt.datetime.now().year).scrape_prob()
    print(f'Win Prob {win_prob}')
    ti.xcom_push(key='win_prob',value=win_prob)