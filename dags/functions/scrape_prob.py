import requests
from bs4 import BeautifulSoup
import os.path


def scrape_prob(short_team_name):
    url = 'https://projects.fivethirtyeight.com/2023-mlb-predictions/games/'
    page = requests.get(url)

    soup = BeautifulSoup(page.content, 'html.parser')   
    results_team = soup.find_all('span',class_='team-name short')
    results_win_prob = soup.find('main',class_='container').find('table',class_='table').find_all('td', class_="td number td-number win-prob")

    team_i=0
    for team in results_team:
        if team.get_text()== short_team_name:
            team_pct_i=team_i
            break
        team_i+=1

    prob_win = results_win_prob[team_pct_i].get_text()

    return prob_win


if __name__=='__main__':
    yanks_prob = scrape_prob('NYY')
    print(yanks_prob)