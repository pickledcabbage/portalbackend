import boto3
from src.enums.enums import player_status

class DBAccessor:

    def __init__(self):
        self.PLAYERS_TABLE = 'Players'
        self.COURTS_TABLE = 'Courts'
        self.QUEUE_TABLE = 'Queue'
        self.CONFIG_TABLE = 'Config'
        self.QUEUE_TOKEN = 'QueueToken'
        self.MAIN_QUEUE = 'MainQueue'
        url = "http://localhost:8000"
        self.client = boto3.client('dynamodb', region_name='us-west-2', endpoint_url=url)
    
    # For test purposes
    def get_table_names(self):
        return self.client.list_tables()["TableNames"]

    def get_config_token(self):
        token = self.client.get_item(
            TableName=self.CONFIG_TABLE,
            Key={
                'config-name': {
                    'S': self.QUEUE_TOKEN
                }
            }
            )['Item']
        updated_token = token.copy()
        updated_token['last']['N'] = str(int(updated_token['last']['N'])+1)
        self.client.put_item(
            TableName=self.CONFIG_TABLE,
            Item=updated_token
        )
        return token
    
    def get_player(self, player_id):
        player = self.client.get_item(
            TableName=self.PLAYERS_TABLE,
            Key={
                'id' : {
                    'S': player_id
                }
            }
        )
        if ('Item' in player):
            return player['Item']
        return None
    
    def create_player(self, player):
        return self.client.put_item(
            TableName=self.PLAYERS_TABLE,
            Item=player
        )

    def update_player_status(self, username, status, token_last):
        player = self.get_player(username)
        if player is not None:
            player['status']['S'] = str(status)
            player['queue-position'] = token_last
            self.create_player(player)
    
    def get_courts(self):
        return self.client.scan(
            TableName=self.COURTS_TABLE
        )['Items']

    def add_to_queue(self, token_last, players):
        for i in players:
            self.update_player_status(i, player_status.IN_QUEUE, token_last)
        self.client.put_item(
            TableName=self.QUEUE_TABLE,
            Item={
                'queue-name': { 'S': self.MAIN_QUEUE},
                'position': token_last,
                'players':{ 'L': [ { 'S': i } for i in players ] }
            }
        )

