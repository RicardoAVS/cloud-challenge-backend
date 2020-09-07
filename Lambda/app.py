import json
import boto3
import os

# Initialize dynamodb boto3 object
dynamodb = boto3.resource('dynamodb')

# Set dynamodb table name variable from env
table = dynamodb.Table(os.environ['databaseName'])
print(os.environ['databaseName'])


def increment_visit(counter):

    # Add item to Table and return
    response = table.update_item(
        Key={
            'SourceIP': counter
        },
        UpdateExpression='ADD visit_count :value',
        ExpressionAttributeValues={
            ':value': 1
        },
        ReturnValues="UPDATED_NEW"
    )

    return response


def lambda_handler(event, context):
    data = json.loads(event["body"])

    update_item = increment_visit(data['Website'])

    # Create api response object
    return {
        "isBase64Encoded": 'false',
        "statusCode": 200,
        'headers': {
            'Access-Control-Allow-Headers': '*',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST'
        },
        "body": json.dumps({
            'count': int(update_item['Attributes']['visit_count'])
        })
    }
