import boto3
import time
import requests

s3 = boto3.client('s3')

# The S3 bucket name
bucket_name = 'testbucket-weihao'

# The API Gateway URL to trigger the plotting lambda
plotting_api_url = 'https://qnyneu43h7.execute-api.us-east-1.amazonaws.com/plot'  # Replace with your actual API URL


def lambda_handler(event, context):
    # Step 1: Create object 'assignment1.txt'
    s3.put_object(Bucket=bucket_name, Key='assignment1.txt', Body='Empty Assignment 1')
    print("Created 'assignment1.txt' with size 19 bytes")

    # Sleep for some time to create spacing between events
    time.sleep(1)

    # Step 2: Update object 'assignment1.txt'
    s3.put_object(Bucket=bucket_name, Key='assignment1.txt', Body='Empty Assignment 2222222222')
    print("Updated 'assignment1.txt' with size 28 bytes")

    # Sleep for some time
    time.sleep(1)

    # Step 3: Delete object 'assignment1.txt'
    s3.delete_object(Bucket=bucket_name, Key='assignment1.txt')
    print("Deleted 'assignment1.txt'")

    # Sleep for some time
    time.sleep(1)

    # Step 4: Create object 'assignment2.txt'
    s3.put_object(Bucket=bucket_name, Key='assignment2.txt', Body='33')
    print("Created 'assignment2.txt' with size 2 bytes")

    # Sleep for some time
    time.sleep(1)

    # Step 5: Call the Plotting API
    print("Calling the plotting API...")
    response = requests.get(plotting_api_url)

    # Check the response from the API call
    if response.status_code == 200:
        print("Plotting API successfully invoked")
    else:
        print(f"Failed to invoke Plotting API. Status Code: {response.status_code}")

    return {
        'statusCode': 200,
        'body': 'S3 operations and API call completed successfully'
    }
