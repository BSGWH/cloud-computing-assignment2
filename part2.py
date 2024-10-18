import boto3
import time
from decimal import Decimal
from datetime import datetime

s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')


def lambda_handler(event, context):
    bucket_name = 'testbucket-weihao'
    table = dynamodb.Table('S3-object-size-history')

    # Calculate total size and count of objects in the bucket
    total_size = 0
    total_objects = 0

    response = s3.list_objects_v2(Bucket=bucket_name)
    if 'Contents' in response:
        for obj in response['Contents']:
            total_size += obj['Size']
            total_objects += 1

    # Convert current time to human-readable time
    timestamp = Decimal(str(time.time()))
    readable_time = datetime.utcfromtimestamp(float(timestamp)).strftime('%Y-%m-%d %H:%M:%S')

    # Add entry to DynamoDB
    table.put_item(
        Item={
            'bucket_name': bucket_name,
            'timestamp': readable_time,
            'bucket_size': Decimal(str(total_size)),
            'total_objects': Decimal(str(total_objects))
        }
    )

    return {
        'statusCode': 200,
        'body': f'Updated size {total_size} bytes with {total_objects} objects.'
    }
