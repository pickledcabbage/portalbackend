import boto3
from src.db.translators import QueueTranslator

PLAYERS_TABLE = 'Players'
COURTS_TABLE = 'Courts'
QUEUE_TABLE = 'Queue'
CONFIG_TABLE = 'Config'
QUEUE_TOKEN = 'QueueToken'
MAIN_QUEUE = 'MainQueue'
url = "http://localhost:8000"
client = boto3.client('dynamodb', region_name='us-west-2', endpoint_url=url)

qt = QueueTranslator()

for i in client.scan(TableName=QUEUE_TABLE)['Items']:
    print(qt.fromDb(i))