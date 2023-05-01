import json
import boto3
import csv

def get_content(s3_client,record):
    try:
        s3_bucket = record['s3']['bucket']['name']
        object_key = record['s3']['object']['key']
        file_content = str(s3_client.get_object(
            Bucket=s3_bucket, Key=object_key)["Body"].read()).split('\\n')[1].split(',')
        away_team = file_content[0]
        home_team = file_content[1]
        away_pitcher = file_content[2]
        home_pitcher = file_content[3]
        ballpark = file_content[4][:-2]
        message = f'The {away_team} are playing against the {home_team} at {ballpark}.\n{away_pitcher} is pitching against {home_pitcher}.'
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
    message = get_content(s3_client,record)
    subject = f'Upcoming Yankee Game'
    topic_arn = 'arn:aws:sns:us-west-2:524377119254:MLBTopic'
    send_sns(message, subject, topic_arn)