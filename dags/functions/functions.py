import requests
from bs4 import BeautifulSoup
import datetime as dt

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

class datetimeChange:
    '''
    Change time from datetime in UTC to just time in Eastern time zone.
    '''
    def __init__(self, orig_datetime):
        self.orig_datetime = orig_datetime
    
    def hr24_to_hr12(self):
        new_time_24_hr = dt.datetime.strptime(self.orig_datetime, '%Y-%m-%dT%H:%M:%SZ') - dt.timedelta(hours=4)
        new_time_12_hr = new_time_24_hr.strftime('%I:%M PM').lstrip('0')
        return new_time_12_hr
