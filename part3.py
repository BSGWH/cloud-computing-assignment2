import boto3
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Initialize clients
dynamodb = boto3.resource('dynamodb')
s3 = boto3.client('s3')

def lambda_handler(event, context):
    bucket_name = 'testbucket-weihao'
    table_name = 'S3-object-size-history'

    # Get DynamoDB table
    table = dynamodb.Table(table_name)

    # Get current time and 10 seconds ago as human-readable strings
    now = datetime.utcnow()
    ten_seconds_ago = now - timedelta(seconds=10)
    now_str = now.strftime('%Y-%m-%d %H:%M:%S')
    ten_seconds_ago_str = ten_seconds_ago.strftime('%Y-%m-%d %H:%M:%S')

    # Query DynamoDB for the last 10 seconds
    response = table.query(
        KeyConditionExpression=boto3.dynamodb.conditions.Key('bucket_name').eq(bucket_name) &
                               boto3.dynamodb.conditions.Key('timestamp').between(ten_seconds_ago_str, now_str)
    )

    items = response['Items']

    if not items:
        return {
            'statusCode': 200,
            'body': 'No data found in the last 10 seconds.'
        }

    # Extract timestamps and sizes from DynamoDB items
    timestamps = [item['timestamp'] for item in items]
    sizes = [float(item['bucket_size']) for item in items]

    # Convert string timestamps back to datetime objects for plotting
    timestamps_dt = [datetime.strptime(ts, '%Y-%m-%d %H:%M:%S') for ts in timestamps]

    # Find the maximum size from the retrieved bucket sizes
    max_size = max(sizes) if sizes else 0

    # Plot the data
    plt.figure()
    plt.plot(timestamps_dt, sizes, label='Bucket Size Over Time', marker='o')
    plt.axhline(y=max_size, color='r', linestyle='--', label='Max Size in Last 10 Seconds')
    plt.xlabel('Timestamp')
    plt.ylabel('Size (bytes)')
    plt.legend()

    # Save the plot locally and upload to S3
    plot_file = '/tmp/plot.png'
    plt.savefig(plot_file)

    with open(plot_file, 'rb') as data:
        s3.put_object(Bucket=bucket_name, Key='plot.png', Body=data)

    return {
        'statusCode': 200,
        'body': 'Plot created and uploaded to S3 successfully.'
    }
