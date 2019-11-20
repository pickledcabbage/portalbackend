from src.db.dba import DBAccessor
from src.enums.enums import player_status
from src.error.QueueError import QueueError

def logic_signup_group(players):
    dba = DBAccessor()
    bad_players = []
    signed_up_players = []
    for i in players:
        p = dba.get_player(i)
        if p is None:
            bad_players.append(p)
        elif p['status']['S'] != str(player_status.IDLE):
            signed_up_players.append(p)
    for i in signed_up_players:
        print(i)
    if (bad_players != [] or signed_up_players != []):
        raise QueueError('Failed to sign up players')

    token = dba.get_config_token()['last']
    dba.add_to_queue(token, players)

    return {"Message": "Successfully signed up!"}