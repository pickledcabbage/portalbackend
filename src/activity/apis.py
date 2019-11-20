from src.logic.player_logic import *
from src.logic.queue_logic import *
from src.error.ServiceError import ServiceError
from src.error.QueueError import QueueError

def api_add_player(player):

    # check if all required things are there
    if ('name' not in player or 'username' not in player):
        raise ServiceError('some values not provided!')
    return logic_signup_player(player['username'],player['name'])

def api_signup_group(group):

    if ('players' not in group):
        raise ServiceError('Group not passed!')
    if (len(group['players']) != 4):
        raise QueueError('Must sign up with 4 players!')
    return logic_signup_group(group['players'])
