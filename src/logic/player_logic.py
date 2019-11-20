from src.db.dba import DBAccessor
from src.enums.enums import player_status


# no check done, just simply signs up player
def logic_signup_player(username,name):
    dba = DBAccessor()

    player = dba.get_player(username)
    if player is None:
        player = builder_player(username,name)
        dba.create_player(player)
    return player




def builder_player(username, name):
    return {
        'id': {'S': username},
        'name': {'S': name},
        'court': {'S': 'N/A'},
        'status': {'S': str(player_status.IDLE)}
    }