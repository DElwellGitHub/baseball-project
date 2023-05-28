# Daily alerts for Major League Baseball games
### A project that uses Airflow and AWS (EC2, Lambda and SNS) to send an automated alert about today's Yankee game

<p>As a developer and New York Yankees fan, I wanted to practice my data engineering skills by setting up a daily alert that would give me info about today's upcoming Yankee game.
This project uses Apache Airflow, an open-source orchestration tool developed by Airbnb, along with several Amazon Web Services (EC2, Lambda and SNS) to send a daily alert. 

To get the data needed, I use an API for Major League Baseball stats, and I webscrape [FiveThirtyEight's MLB games predictions page](https://projects.fivethirtyeight.com/2023-mlb-predictions/games/) in order to show the odds of the Yankees winning. The resulting message looks similar to this:
</p>

![image](https://github.com/DElwell90/baseball-project/assets/26678347/42d2d335-4dc1-415f-9307-637fd22dd62e)

### Data pipeline
![Flowcharts (1)](https://github.com/DElwell90/baseball-project/assets/26678347/994d5f54-49cf-42d3-8510-27c503729620)


### MLB API
<p>In order to efficiently call MLB stats data, I leveraged a popular [Python wrapper for MLB's API](https://pypi.org/project/MLB-StatsAPI/), created by Todd Roberts. The Python wrapper allows me to directly call MLB's API for important data needed for my alert: </p>
- Wins
- Losses
- Games back of first place
- Who the Yankees are playing
- Which ballpark they are playing in
- Starting pitchers
- Game time


### FiveThirtyEight webscraping
<p> FiveThirtyEight is known primarily for its data-based journalism and political polling aggregation, however it is also a great resource for seeing predictions on games in all major sports, including Major League Baseball. On gamedays, FiveThirtyEight will post chance of winning odds, as shown in the image below:


Talk about FiveThirtyEight odds and how we scrape it <br>
Include screenshot of website


### Airflow Dag
Include dag graph

### Setup
How I set up airflow using docker <br>
How I set up EC2 to only run for about 20 min a day using lambda start and stop functions

### Conclusion
What I learned <br>
How this can be applied for other things.
