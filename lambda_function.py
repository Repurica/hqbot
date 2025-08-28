import json
import boto3
import requests  # If added via layer or package

def lambda_handler(event, context):
    # Your code here
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }