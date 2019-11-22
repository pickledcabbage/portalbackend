import boto3
from src.db.translators import CourtTranslator

def CTD():
    PLAYERS_TABLE = 'Players'
    COURTS_TABLE = 'Courts'
    QUEUE_TABLE = 'Queue'
    CONFIG_TABLE = 'Config'
    QUEUE_TOKEN = 'QueueToken'
    MAIN_QUEUE = 'MainQueue'
    url = "http://localhost:8000"
    client = boto3.client('dynamodb', region_name='us-west-2', endpoint_url=url)

    ct = CourtTranslator()

    for i in client.scan(TableName=COURTS_TABLE)['Items']:
        print(ct.fromDb(i))

if __name__ == "__main__":
    CTD()