import boto3
import pytest
from moto import mock_dynamodb2

AWS_REGION = 'us-east-1'
TABLE_NAME = 'TestDataBase'

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
        "origin": "191.95.153.33",
        "Referer": "http://software-student.me/",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "cross-site",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36",
        "Via": "2.0 0114bca509b46f77e118f6ce3220e769.cloudfront.net (CloudFront)",
        "X-Amz-Cf-Id": "EBwx0Tt-SYmMBxDYQCPEZcCeGU4bhZEXmNwjgdVNuYlgTazz6q-Kag==",
        "X-Amzn-Trace-Id": "Root=1-5f467f37-0f7a040c220cbe747d187fac",
        "X-Forwarded-For": "191.95.153.33, 64.252.186.79",
        "X-Forwarded-Port": "443",
        "X-Forwarded-Proto": "https"
    },
    "multiValueHeaders": {
        "Accept": [
            "*/*"
        ],
        "Accept-Encoding": [
            "gzip, deflate, br"
        ],
        "Accept-Language": [
            "fr-CA,fr;q=0.9,es-CO;q=0.8,es-US;q=0.7,es;q=0.6,en-US;q=0.5,en;q=0.4"
        ],
        "CloudFront-Forwarded-Proto": [
            "https"
        ],
        "CloudFront-Is-Desktop-Viewer": [
            "true"
        ],
        "CloudFront-Is-Mobile-Viewer": [
            "false"
        ],
        "CloudFront-Is-SmartTV-Viewer": [
            "false"
        ],
        "CloudFront-Is-Tablet-Viewer": [
            "false"
        ],
        "CloudFront-Viewer-Country": [
            "CO"
        ],
        "content-type": [
            "application/json"
        ],
        "Host": [
            "zweaywp9rg.execute-api.us-east-1.amazonaws.com"
        ],
        "origin": [
            "191.95.153.33"
        ],
        "Referer": [
            "http://software-student.me/"
        ],
        "sec-fetch-dest": [
            "empty"
        ],
        "sec-fetch-mode": [
            "cors"
        ],
        "sec-fetch-site": [
            "cross-site"
        ],
        "User-Agent": [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36"
        ],
        "Via": [
            "2.0 0114bca509b46f77e118f6ce3220e769.cloudfront.net (CloudFront)"
        ],
        "X-Amz-Cf-Id": [
            "EBwx0Tt-SYmMBxDYQCPEZcCeGU4bhZEXmNwjgdVNuYlgTazz6q-Kag=="
        ],
        "X-Amzn-Trace-Id": [
            "Root=1-5f467f37-0f7a040c220cbe747d187fac"
        ],
        "X-Forwarded-For": [
            "191.95.153.33, 64.252.186.79"
        ],
        "X-Forwarded-Port": [
            "443"
        ],
        "X-Forwarded-Proto": [
            "https"
        ]
    },
    "queryStringParameters": "None",
    "multiValueQueryStringParameters": "None",
    "pathParameters": "None",
    "stageVariables": "None",
    "requestContext": {
        "resourceId": "8j9yaf",
        "resourcePath": "/visitors",
        "httpMethod": "POST",
        "extendedRequestId": "R4jQuE9woAMFflA=",
        "requestTime": "26/Aug/2020:15:26:47 +0000",
        "path": "/Prod/visitors",
        "accountId": "722486161107",
        "protocol": "HTTP/1.1",
        "stage": "Prod",
        "domainPrefix": "zweaywp9rg",
        "requestTimeEpoch": 1598455607709,
        "requestId": "3f43b0d8-2412-4848-8604-c9cfb86dc713",
        "identity": {
            "cognitoIdentityPoolId": "None",
            "accountId": "None",
            "cognitoIdentityId": "None",
            "caller": "None",
            "sourceIp": "191.95.153.33",
            "principalOrgId": "None",
            "accessKey": "None",
            "cognitoAuthenticationType": "None",
            "cognitoAuthenticationProvider": "None",
            "userArn": "None",
            "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36",
            "user": "None"
        },
        "domainName": "zweaywp9rg.execute-api.us-east-1.amazonaws.com",
        "apiId": "zweaywp9rg"
    }
}


@pytest.fixture
def environment_variables(monkeypatch):
    monkeypatch.setenv("AWS_REGION", AWS_REGION)
    monkeypatch.setenv("TABLE_NAME", TABLE_NAME)


@mock_dynamodb2
def test_dynamodb_setup():
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

        from Lambda.app import lambda_handler

        test_body = {
            'body': '{\"Website\": \"Test\"}',
            **test_event
        }

        ret = lambda_handler(test_body, "")
        return ret


@pytest.fixture()
def test_lambda_api(environment_variables):

    test_status_code = {
        'status_code': 200,
        'test_key': 'count',
        'test_type': int
    }

    ret = test_dynamodb_setup()

    assert ret["statusCode"] == test_status_code["status_code"]
