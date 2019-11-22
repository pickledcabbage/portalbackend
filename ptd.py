import boto3
from src.db.translators import PlayerTranslator

def PTD():
    PLAYERS_TABLE = 'Players'
    COURTS_TABLE = 'Courts'
    QUEUE_TABLE = 'Queue'
    CONFIG_TABLE = 'Config'
    QUEUE_TOKEN = 'QueueToken'
    MAIN_QUEUE = 'MainQueue'
    url = "http://localhost:8000"
    client = boto3.client('dynamodb', region_name='us-west-2', endpoint_url=url)

    pt = PlayerTranslator()

    for i in client.scan(TableName=PLAYERS_TABLE)['Items']:
        print(pt.fromDb(i))

if __name__ == "__main__":
    PTD()