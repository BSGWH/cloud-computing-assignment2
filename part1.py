import boto3
import os

# Initialize boto3 clients for DynamoDB and S3
dynamodb = boto3.resource('dynamodb')
s3 = boto3.client('s3')



def create_s3_bucket(bucket_name):
    try:
        # Create S3 bucket
        s3.create_bucket(Bucket=bucket_name)
        print(f"S3 bucket '{bucket_name}' created successfully.")
    except Exception as e:
        print(f"Error creating S3 bucket: {e}")

def create_dynamodb_table(table_name):
    try:
        # Create DynamoDB table
        table = dynamodb.create_table(
            TableName=table_name,
            KeySchema=[
                {
                    'AttributeName': 'bucket_name',
                    'KeyType': 'HASH'
                },
                {
                    'AttributeName': 'timestamp',
                    'KeyType': 'RANGE'
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'bucket_name',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'timestamp',
                    'AttributeType': 'S'
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        print(f"DynamoDB table '{table_name}' created successfully.")
    except Exception as e:
        print(f"Error creating DynamoDB table: {e}")

def main():
    bucket_name = 'testbucket-weihao'
    table_name = 'S3-object-size-history'

    # Create S3 bucket
    create_s3_bucket(bucket_name)

    # Create DynamoDB table
    create_dynamodb_table(table_name)

if __name__ == '__main__':
    main()

