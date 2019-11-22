from src.db.PlayerDBA import PlayerDBA
from src.enums.enums import player_status
from src.logic.queue_logic import _drop_from_queue
from src.logic.court_logic import _drop_from_court
from src.error.ServiceError import ServiceError


# no check done, just simply signs up player
def logic_signup_player(username,name):
    pdba = PlayerDBA()

    player = pdba.get_player(username)
    if player is None:
        player = builder_player(username,name)
        pdba.put_player(player)
    return player

def logic_player_drop(username):
    pdba = PlayerDBA()
    player = pdba.get_player(username)
    if player is None:
        return
    
    if player['status'] == str(player_status.IN_QUEUE):
        _drop_from_queue(player)
    if player['status'] == str(player_status.ON_COURT):
        _drop_from_court(player)

def logic_get_status(username):
    pdba = PlayerDBA()
    player = pdba.get_player(username)
    if player is None:
        raise ServiceError('User not found!')
    return {
        'status': player['status'],
        'court': player['court']
    }



def builder_player(username, name):
    return {
        'id': username,
        'name': name,
        'court': 'N/A',
        'status': str(player_status.IDLE)
    }