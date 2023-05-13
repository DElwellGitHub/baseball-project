import requests
from bs4 import BeautifulSoup
import os.path

url = 'https://projects.fivethirtyeight.com/2023-mlb-predictions/games/'
page = requests.get(url)

soup = BeautifulSoup(page.content, 'html.parser')


#results = soup.find('table',class_='table').find('tbody').find('tr',class_='tr').find('td', class_="td td-team team").find('span',class_='team-name short')
results_team = soup.find_all('span',class_='team-name short')

results_win_prob = soup.find('main',class_='container').find('table',class_='table').find_all('td', class_="td number td-number win-prob")

team_i=0
for team in results_team:
    if team.get_text()== 'NYY':
        team_pct_i=team_i
        break
    team_i+=1

print(results_win_prob[team_pct_i].get_text())


# save_path = '/home/ubuntu/airflow-docker/'
# full_name = os.path.join(save_path, 'read_file'+'.txt')

# file1 = open(full_name,'w')

# file1.write(str(soup.prettify()))

# file1.close()

# full_name2 = os.path.join(save_path, 'parsed_file'+'.txt')
# file2 = open(full_name2,'w')
# file2.write(str(results.prettify()))
# file2.close()

# print('hello there')