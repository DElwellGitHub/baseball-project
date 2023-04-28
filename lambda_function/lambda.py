import json
import boto3

topic_arn = "arn:aws:sns:us-west-2:524377119254:MLBTopic"
def send_sns(message, subject):
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

s3_client = boto3.client('s3')
S3_BUCKET_NAME = 's3://mlb-project/'


def lambda_handler(event, context):
    object_key = "games/games (2023-04-28).csv"  # replace object key
    file_content = s3_client.get_object(
        Bucket=S3_BUCKET, Key=object_key)["Body"].read()
    print(file_content)

'''
def lambda_handler(event, context):
    print("event collected is {}".format(event))
    for record in event['Records'] :
        s3_bucket = record['s3']['bucket']['name']
        print("Bucket name is {}".format(s3_bucket))
        s3_key = record['s3']['object']['key']
        print("Bucket key name is {}".format(s3_key))
        from_path = "s3://{}/{}".format(s3_bucket, s3_key)
        print("from path {}".format(from_path))
        
        #TODO get games from csv
        object_key = "OBJECT_KEY"  # replace object key
        file_content = s3_client.get_object(
        Bucket=S3_BUCKET, Key=object_key)["Body"].read()
        print(file_content)
        # s3 = boto3.resource('s3')
        # new_file_key = os.path.join('/tmp', file_name)
        # s3.Bucket('bucketname').download_file(file_key, new_file_key)
       
        # with open('s3://mlb-project/games/games (2023-04-28).csv', encoding='utf-8') as f:
        #     for row in f:
        #         print(f)
        
        
        
        message = "The file is uploaded at S3 bucket path {}".format(from_path)
        subject = "Processes completion Notification"
        SNSResult = send_sns(message, subject)
        if SNSResult :
            print("Notification Sent..") 
            return SNSResult
        else:
            return False
'''