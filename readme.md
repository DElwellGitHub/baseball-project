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
<p> FiveThirtyEight is known primarily for its data-based journalism and political polling aggregation, however it is also a great resource for seeing predictions on games in all major sports, including Major League Baseball. On gamedays, FiveThirtyEight will post chance of winning odds, as shown in the far-right column in the image below:</p>

![FiveThirtyEight](https://github.com/DElwell90/baseball-project/assets/26678347/5d10046f-1a3d-44c4-b858-bebd565b55fe)

Using two popular Python libraries, I scrape FiveThirtyEight's website in order to automatically pull the Yankees' odds of winning on today's date, which later is brought into my email essage.

### Airflow Dag
<p> As an open-source orchestration tool, Airflow serves as a great way to schedule and execute all tasks needed in order to pull my data and organize it for my message. It's workflow can be summarized by the following steps: </p>

1. Start directed acyclic graph (dag).
2. Call MLB's API to get today's games data (i.e. who is playing today).

3. Check if there is a Yankee game today. If not, end dag. If there is, then proceed to next step.

4. Call MLB's standings data to get teams' wins, losses and games back.

5. Scrape FiveThirtyEight's website to get Yankees' probability of winning.
6. Create a Postgres SQL table that will organize all of our data.
7. Write a SQL insert query for our data.
8. Execute the insert query.
9. Send the Postgres table data to a csv and place in an S3 bucket.
10. Delete Xcoms data (Xcoms is local storage used for our Airflow dag).
11. End dag.

<p>Here is the screenshot of my dag: </p>

![dag](https://github.com/DElwell90/baseball-project/assets/26678347/d62a4a6d-c270-43b9-95ef-c00cd9bab423)



### Setup
How I set up airflow using docker <br>
How I set up EC2 to only run for about 20 min a day using lambda start and stop functions

### Conclusion
What I learned <br>
How this can be applied for other things.
