import boto3
import pytest
from moto import mock_dynamodb2

AWS_REGION = 'us-east-1'
TABLE_NAME = 'TestTable'

test_event = {
    "resource": "/visitors",
    "path": "/visitors",
    "httpMethod": "POST",
    "headers": {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "fr-CA,fr;q=0.9,es-CO;q=0.8,es-US;q=0.7,es;q=0.6,en-US;q=0.5,en;q=0.4",
        "CloudFront-Forwarded-Proto": "https",
        "CloudFront-Is-Desktop-Viewer": "true",
        "CloudFront-Is-Mobile-Viewer": "false",
        "CloudFront-Is-SmartTV-Viewer": "false",
        "CloudFront-Is-Tablet-Viewer": "false",
        "CloudFront-Viewer-Country": "CO",
        "content-type": "application/json",
        "Host": "zweaywp9rg.execute-api.us-east-1.amazonaws.com",
        "origin": "127.0.0.1",
        "Referer": "",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "cross-site",
        "Via": "2.0 0114bca509b46f77e118f6ce3220e769.cloudfront.net (CloudFront)",
        "X-Amz-Cf-Id": "EBwx0Tt-SYmMBxDYQCPEZcCeGU4bhZEXmNwjgdVNuYlgTazz6q-Kag==",
        "X-Amzn-Trace-Id": "Root=1-5f467f37-0f7a040c220cbe747d187fac",
        "X-Forwarded-For": "`127.0.0.1, target.ip.address",
        "X-Forwarded-Port": "443",
        "X-Forwarded-Proto": "https"
    }
}


@pytest.fixture()
def environment_variables(monkeypatch):
    monkeypatch.setenv("AWS_REGION", AWS_REGION)
    monkeypatch.setenv("databaseName", TABLE_NAME)


@mock_dynamodb2
def dynamodb_setup():
    with mock_dynamodb2():

        dynamodb = boto3.resource('dynamodb', AWS_REGION)
        dynamodb.create_table(
            TableName=TABLE_NAME,
            KeySchema=[
                {
                    "AttributeName": "SourceIP",
                    "KeyType": "HASH"
                }
            ],
            AttributeDefinitions=[
                {
                    "AttributeName": "SourceIP",
                    "AttributeType": "S"
                }],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )

        test_body = {
            'body': '{\"Website\": \"Test\"}',
            **test_event
        }
        from Lambda.app import lambda_handler

        res = lambda_handler(test_body, "")
        return res


def test_lambda_api(environment_variables):

    test_status_code = {
        'status_code': 200,
        'test_key': 'count',
        'test_type': int
    }

    res = dynamodb_setup()

    assert res["statusCode"] == test_status_code["status_code"]
