from src.enums.enums import player_status
from src.db.DBA import DBA
from src.db.translators import PlayerTranslator

class PlayerDBA(DBA):

    def __init__(self):
        self.PLAYERS_TABLE = 'Players'
        self.pt = PlayerTranslator()
        DBA.__init__(self)
    
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
            return self.pt.fromDb(player['Item'])
        return None
    
    def put_player(self, player):
        self.client.put_item(
            TableName=self.PLAYERS_TABLE,
            Item=self.pt.toDB(player)
        )
        return "Created player!"

    def update_player_status(self, username, status, token_last):
        player = self.get_player(username)
        if player is not None:
            player['status'] =  str(status)
            player['queue-position'] = token_last
            self.put_player(player)