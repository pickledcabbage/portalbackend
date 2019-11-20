import boto3
from src.enums.enums import player_status

class DBA:
    def __init__(self):
        url = "http://localhost:8000"
        self.client = boto3.client('dynamodb', region_name='us-west-2', endpoint_url=url)
    
    # For test purposes
    def get_table_names(self):
        return self.client.list_tables()["TableNames"]


    

