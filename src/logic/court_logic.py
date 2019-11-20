from src.db.CourtDBA import CourtDBA
from src.db.PlayerDBA import PlayerDBA

def _drop_from_court(player):
    cdba = CourtDBA()
    pdba = PlayerDBA()
    court_id = player['court']

    cdba.clear_court(court_id)
    
