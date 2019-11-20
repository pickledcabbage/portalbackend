from src.db.CourtDBA import CourtDBA
from src.db.PlayerDBA import PlayerDBA

def _drop_from_court(player):
    cdba = CourtDBA()
    pdba = PlayerDBA()
    court_id = player['court']

    players = cdba.clear_court(court_id)

    for i in players:
        pdba.update_player_status(i, player_status.IDLE, '0')
    
    # create a new thread a run refresh
    
