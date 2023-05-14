import json
import boto3
import csv
import datetime as dt

def get_subject_content(s3_client,record):
    #get subject content
    try:
        s3_bucket = record['s3']['bucket']['name']
        object_key = record['s3']['object']['key']
        file_content = str(s3_client.get_object(
            Bucket=s3_bucket, Key=object_key)["Body"].read()).split('\\n')[1].split(',')
        today_date = dt.datetime.now().strftime('%b %d, %Y')
        game_time = file_content[13][:-2]
        subject = f'Upcoming Yankee Game {today_date} at {game_time}'
        print(subject)
        return subject
    except Exception as e:
        print('Error occured while constructing subject: ', e)
        return True

def get_message_content(s3_client,record):
    #get message content
    try:
        s3_bucket = record['s3']['bucket']['name']
        object_key = record['s3']['object']['key']
        file_content = str(s3_client.get_object(
            Bucket=s3_bucket, Key=object_key)["Body"].read()).split('\\n')[1].split(',')
        away_team = file_content[0]
        home_team = file_content[1]
        away_pitcher = file_content[2]
        home_pitcher = file_content[3]
        ballpark = file_content[4]
        date = file_content[5]
        home_wins = file_content[6]
        home_losses = file_content[7]
        home_gb = file_content[8]
        away_wins = file_content[9]
        away_losses = file_content[10]
        away_gb = file_content[11]
        team_win_prob = file_content[12]
        game_time = file_content[13][:-2]
        message = f'''The {away_team} ({away_wins}-{away_losses}, {away_gb} games back) are playing against the {home_team} ({home_wins}-{home_losses}, {home_gb} games back) at {ballpark}.
{away_pitcher} is pitching against {home_pitcher}.
Game time is {game_time}.
Yankees have a {team_win_prob} chance of winning, according to FiveThirtyEight.
                        '''
        print(message)
        return message
    except Exception as e:
        print('Error occured while constructing message: ', e)
        return True

def send_sns(message, subject, topic_arn):
    try:
        client = boto3.client("sns")
        result = client.publish(TopicArn=topic_arn, Message=message, Subject=subject)
        if result['ResponseMetadata']['HTTPStatusCode'] == 200:
            print(result)
            print("Notification send successfully..!!!")
            return True
    except Exception as e:
        print("Error occured while publish notifications and error is : ", e)
        return True

def lambda_handler(event, context):
    s3_client = boto3.client('s3')
    record = event['Records'][0]
    print(record)
    message = get_message_content(s3_client,record)
    today_date = dt.datetime.now().strftime('%b %d, %Y')
    subject = get_subject_content(s3_client,record)
    topic_arn = 'arn:aws:sns:us-west-2:524377119254:MLBTopic'
    send_sns(message, subject, topic_arn)