# run this before importing boto3 to set proper time
import os
os.environ["TZ"] = "UTC"

import boto3

def CREATE_COURTS():
    client = boto3.client('dynamodb', region_name='us-west-2', endpoint_url="http://localhost:8000")

    # adds standard court setup at UW Badminton, 4x Free-Play Courts
    COURTS_TABLE = 'Courts'

    for i in range(1,5):
        client.put_item(
            TableName= COURTS_TABLE,
            Item={
                'id': {'S': 'uw-court-'+str(i)},
                'name': {'S': 'Court ' + str(i)},
                'type': {'S': 'Free-Play'},
                'players': {'L': []},
                'occupied': {'BOOL': False}
            }
        )

if __name__ == "__main__":
    CREATE_COURTS()