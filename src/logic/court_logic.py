from src.db.CourtDBA import CourtDBA
from src.db.PlayerDBA import PlayerDBA
from src.enums.enums import player_status
from src.logic.RefreshThread import RefreshThread

def logic_get_court_data():
    cdba = CourtDBA()

    return cdba.get_courts()

def _drop_from_court(player):
    cdba = CourtDBA()
    pdba = PlayerDBA()
    court_id = player['court']

    players = cdba.get_court(court_id)['players']

    if player['id'] in players:
        print("here!")
        cdba.clear_court(court_id)
        for i in players:
            pdba.update_player_status(i, status=player_status.IDLE)
        rt = RefreshThread()
        rt.start()
    else:
        print("nope!")
        print(player['id'])
        pdba.update_player_status(player['id'], status=player_status.IDLE)