# Daily alerts for Major League Baseball games
### A project that uses Airflow and AWS (EC2, Lambda and SNS) to send an automated alert about today's Yankee game

<p>As a developer and New York Yankees fan, I wanted to practice my data engineering skills by setting up a daily alert that would give me info about today's upcoming Yankee game.
This project uses Apache Airflow, an open-source orchestration tool developed by Airbnb, along with several Amazon Web Services (EC2, Lambda and SNS) to send a daily alert. 

To get the data needed, I use an API for Major League Baseball stats, and I webscrape [FiveThirtyEight's MLB games predictions page](https://projects.fivethirtyeight.com/2023-mlb-predictions/games/) in order to show the odds of the Yankees winning. The resulting message looks similar to this:
</p>

![image](https://github.com/DElwell90/baseball-project/assets/26678347/42d2d335-4dc1-415f-9307-637fd22dd62e)

### Data pipeline
Include image of data pipeline and explanation

### MLB API
Include reference to statsapi API wrapper and the stats we get

### FiveThirtyEight webscraping
Talk about FiveThirtyEight odds and how we scrape it <br>
Include screenshot of website

### Setup
How I set up airflow using docker <br>
How I set up EC2 to only run for about 20 min a day using lambda start and stop functions

### Conclusion
What I learned <br>
How this can be applied for other things.
