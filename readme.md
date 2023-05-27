# Daily alerts for Major League Baseball games
### A project that uses Airflow and AWS (EC2, Lambda and SNS) to send an automated alert about today's Yankee game

<p>As a developer and New York Yankees fan, I wanted to practice my Data Engineering skills by setting up a daily alert that would give me info about today's upcoming Yankee game.
This project uses Apache Airflow, an open-source orchestration tool developed by Airbnb, along with several Amazon Web Services (EC2, Lambda and SNS) to send a daily alert. 

To get the data needed, I use an API for Major League Baseball stats, and I webscrape FiveThirtyEight's MLB predictions page in order to show the odds of the Yankees winning. The resulting message looks similar to this: test
</p>

![image](https://github.com/DElwell90/baseball-project/assets/26678347/42d2d335-4dc1-415f-9307-637fd22dd62e)
