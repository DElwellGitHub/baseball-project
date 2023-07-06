import datetime as dt
from bs4 import BeautifulSoup
import requests
class scrapeProb:
    '''
    Scrape FiveThirtyEight and get probability that MLB team will win their game.
    '''

    def __init__(self, short_team_name, long_team_name, datetime_now):
        self.short_team_name = short_team_name
        self.long_team_name = long_team_name
        self.year = datetime_now.year
        self.month = datetime_now.month
        self.day = datetime_now.day

    def scrape_prob(self):
        lower_long_team_name = self.long_team_name.lower()
        url = f'https://projects.fivethirtyeight.com/{self.year}-mlb-predictions/{lower_long_team_name}/'
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')

        #Find the day of today's game
        day_location = soup.find('main',class_='container').find('table',class_='table').find('span',class_='day short',string=f'{self.month}/{self.day}')

        #Use that day to locate today's win probability
        prob_win = day_location.findParent().findParent().find_next_sibling().find('td',class_="td number td-number win-prob").get_text()

        return prob_win



def _scrape_prob(ti, short_team_name, long_team_name):
    win_prob = scrapeProb(short_team_name, 
                          long_team_name, 
                          dt.datetime.now()).scrape_prob()
    print(f'Win Prob {win_prob}')
    ti.xcom_push(key='win_prob',value=win_prob)