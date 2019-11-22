from src.enums.enums import player_status
from src.db.DBA import DBA
from src.db.translators import QueueTranslator
from boto3.dynamodb.conditions import Attr, Key

class QueueDBA(DBA):
    def __init__(self):
        self.QUEUE_TABLE = 'Queue'
        self.CONFIG_TABLE = 'Config'
        self.QUEUE_TOKEN = 'QueueToken'
        self.MAIN_QUEUE = 'MainQueue'
        self.qt = QueueTranslator()
        DBA.__init__(self)
    
    def get_config_token(self):
        token = self.client.get_item(
            TableName=self.CONFIG_TABLE,
            Key={
                'config-name': {
                    'S': self.QUEUE_TOKEN
                }
            }
            )['Item']
        token_last = token['last']['N']
        updated_token = token.copy()
        updated_token['last']['N'] = str(int(token_last)+1)
        self.client.put_item(
            TableName=self.CONFIG_TABLE,
            Item=updated_token
        )
        return token_last      

    def get_queue_group(self, token):
        key={
            'queue-name': self.MAIN_QUEUE,
            'position': token
        }
        item = self.client.get_item(
                TableName=self.QUEUE_TABLE,
                Key=self.qt.toDB(key)
            )
        if ('Item' in item):
            return self.qt.fromDb(item['Item'])
        return None

    def add_to_queue(self, token_last, players):
        self.client.put_item(
            TableName=self.QUEUE_TABLE,
            Item={
                'queue-name': { 'S': self.MAIN_QUEUE},
                'position': { 'N': token_last },
                'players':{ 'L': [ { 'S': i } for i in players ] }
            }
        )
    
    def remove_from_queue(self, token_last):
        key={
            'queue-name': self.MAIN_QUEUE,
            'position': token_last
        }
        self.client.delete_item(
            TableName=self.QUEUE_TABLE,
            Key=self.qt.toDB(key)
        )
    
    def queue_position(self, token):
        return self.client.query(
            TableName=self.QUEUE_TABLE,
            KeyConditionExpression='#S = :queue_name AND #T < :position',
            ExpressionAttributeNames={
                '#S': 'queue-name',
                '#T': 'position'
            },
            ExpressionAttributeValues={
                ":queue_name": { 'S': self.MAIN_QUEUE },
                ':position': { 'N': token }
            }
        )['Count']
    
    def pop_from_queue(self):
        query = self.client.query(
            TableName=self.QUEUE_TABLE,
            KeyConditionExpression='#S = :queue_name',
            ExpressionAttributeNames={
                '#S': 'queue-name'
            },
            ExpressionAttributeValues={
                ":queue_name": { 'S': self.MAIN_QUEUE },
            }
        )
        if (len(query['Items']) == 0):
            return None
        items = query['Items']
        lowest = items[0]
        for i in items:
            if (int(i['position']['N']) < int(lowest['position']['N'])):
                lowest = i
        key={
            'queue-name': self.MAIN_QUEUE,
            'position': lowest['position']['N']
        }
        self.client.delete_item(
            TableName=self.QUEUE_TABLE,
            Key=self.qt.toDB(key)
        )
        return self.qt.fromDb(lowest)