# run this before importing boto3 to set proper time
import os
os.environ["TZ"] = "UTC"

import boto3

def CREATE_DB():
    client = boto3.client('dynamodb', region_name='us-west-2', endpoint_url="http://localhost:8000")


    table_list = client.list_tables()["TableNames"]
    PLAYERS_TABLE = 'Players'
    COURTS_TABLE = 'Courts'
    QUEUE_TABLE = 'Queue'
    CONFIG_TABLE = 'Config'
    QUEUE_TOKEN = 'QueueToken'


    # create player table
    if (PLAYERS_TABLE in table_list):
        client.delete_table(
            TableName=PLAYERS_TABLE
        )
    client.create_table(
        AttributeDefinitions=[
            {
                'AttributeName': 'id',
                'AttributeType': 'S'
            }
        ],
        TableName=PLAYERS_TABLE,
        KeySchema=[
            {
                'AttributeName': 'id',
                'KeyType': 'HASH'
            }
        ],
        ProvisionedThroughput= {
            'ReadCapacityUnits': 1,
            'WriteCapacityUnits': 1
        }
    )

    # created courts table
    if (COURTS_TABLE in table_list):
        client.delete_table(
            TableName=COURTS_TABLE
        )
    client.create_table(
        AttributeDefinitions=[
            {
                'AttributeName': 'id',
                'AttributeType': 'S'
            }
        ],
        TableName=COURTS_TABLE,
        KeySchema=[
            {
                'AttributeName': 'id',
                'KeyType': 'HASH'
            }
        ],
        ProvisionedThroughput= {
            'ReadCapacityUnits': 1,
            'WriteCapacityUnits': 1
        }
    )

    # created courts table
    if (QUEUE_TABLE in table_list):
        client.delete_table(
            TableName=QUEUE_TABLE
        )
    client.create_table(
        AttributeDefinitions=[
            {
                'AttributeName': 'queue-name',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'position',
                'AttributeType': 'N'
            }
        ],
        TableName=QUEUE_TABLE,
        KeySchema=[
            {
                'AttributeName': 'queue-name',
                'KeyType': 'HASH'
            },
            {
                'AttributeName': 'position',
                'KeyType': 'RANGE'
            }
        ],
        ProvisionedThroughput= {
            'ReadCapacityUnits': 1,
            'WriteCapacityUnits': 1
        }
    )

    if (CONFIG_TABLE in table_list):
        client.delete_table(
            TableName=CONFIG_TABLE
        )
    client.create_table(
        AttributeDefinitions=[
            {
                'AttributeName': 'config-name',
                'AttributeType': 'S'
            }
        ],
        TableName=CONFIG_TABLE,
        KeySchema=[
            {
                'AttributeName': 'config-name',
                'KeyType': 'HASH'
            }
        ],
        ProvisionedThroughput= {
            'ReadCapacityUnits': 1,
            'WriteCapacityUnits': 1
        }
    )

    client.put_item(
        TableName=CONFIG_TABLE,
        Item={
            'config-name': { 'S': QUEUE_TOKEN},
            'last': { 'N': '0' }
        }
    )

if __name__ == "__main__":
    CREATE_DB()