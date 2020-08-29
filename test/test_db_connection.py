import pytest
import mock
import boto3
from botocore.exceptions import ClientError

TABLE_NAME = 'TestDataBase'

AWS_CREDENTIALS = {
    'aws_access_key_id': '',
    'aws_secret_access_key': '',
    'aws_session_token': ''
}


def dynamodb_setup(dynamodb):
    dynamodb.create_table(
        TableName=TABLE_NAME,
        KeySchema=[
            {
                "AttributeName": "test",
                "KeyType": "HASH"
            }
        ],
        AttributeDefinitions=[
            {
                "AttributeName": "test",
                "AttributeType": "S"
            }],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )


@pytest.fixture
def dynamodb_mock():
    import moto

    with moto.mock_dynamodb2():
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        dynamodb_setup(dynamodb)
        yield dynamodb


@pytest.fixture
def dynamodb():
    dynamodb = boto3.resource('dynamodb', **AWS_CREDENTIALS)

    try:
        dynamodb.Table(TABLE_NAME).delete()
    except ClientError as error:
        if error.__class__.__name__ != 'ResourceNotFoundException':
            raise

    dynamodb_setup(dynamodb)
    dynamodb.meta.client.get_waiter('table_exists').wait(TableName=TABLE_NAME)

    return dynamodb


def test_dynamodb(dynamodb):
    table = dynamodb.Table(TABLE_NAME)

    response = table.put_item(Item={
        'test': '1'
    })

    response = table.get_item(Key={'test': '1'})
    user = response['Item']
    assert user['test'] == '1'

    try:
        dynamodb.Table(TABLE_NAME).delete_item(Key={'test': '1'})
    except ClientError as error:
        response = error.response