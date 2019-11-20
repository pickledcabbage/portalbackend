from src.db.QueueDBA import QueueDBA
from src.db.PlayerDBA import PlayerDBA
from src.enums.enums import player_status
from src.error.QueueError import QueueError

def logic_signup_group(players):
    pdba = PlayerDBA()
    qdba = QueueDBA()
    bad_players = []
    signed_up_players = []
    for i in players:
        p = pdba.get_player(i)
        if p is None:
            bad_players.append(p)
        elif p['status'] != str(player_status.IDLE):
            signed_up_players.append(p)
    for i in signed_up_players:
        print(i)
    if (bad_players != [] or signed_up_players != []):
        raise QueueError('Failed to sign up players')

    token = qdba.get_config_token()

    for i in players:
        pdba.update_player_status(i, player_status.IN_QUEUE, token)

    qdba.add_to_queue(token, players)

    return {"Message": "Successfully signed up!"}

# not equivalent to popping off queue!
def logic_remove_group(username):
    pdba = PlayerDBA()

    player = pdba.get_player(username)
    if (player == None):
        return 'Player not found!'
    if (player['status'] != str(player_status.IN_QUEUE)):
        return 'Player not in queue!'
    
    _drop_from_queue(player)

def _drop_from_queue(player):
    pdba = PlayerDBA()
    qdba = QueueDBA()

    token = player['queue-position']
    qpos = qdba.get_queue_group(token)
    if (qpos == None):
        pdba.update_player_status(player['id'], player_status.IDLE, token)
        return 'Queue group not found, updated player'
    
    qdba.remove_from_queue(token)
    for i in qpos['players']:
        pdba.update_player_status(i, player_status.IDLE, token)
    
    return 'Successfully removed group'