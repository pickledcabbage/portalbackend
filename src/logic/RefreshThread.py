import threading
import time
from src.ThreadHelper import thread_lock
from src.db.QueueDBA import QueueDBA
from src.db.CourtDBA import CourtDBA
from src.db.PlayerDBA import PlayerDBA
from src.enums.enums import player_status

class RefreshThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        # may or may not need this
        self.start_delay = 10
        self.qdba = QueueDBA()
        self.cdba = CourtDBA()
        self.pdba = PlayerDBA()
    
    def run(self):
        thread_lock.acquire()
        try:
            courts = self.cdba.get_courts()
            for i in courts:
                if not i['occupied']:
                    q_top = self.qdba.pop_from_queue()
                    if q_top != None:
                        self.cdba.put_on_court(i['id'], q_top['players'])
                        for j in q_top['players']:
                            self.pdba.update_player_status(j, status=player_status.ON_COURT, court=i['id'])
                        break
        except Exception as e:
            print(e)


        thread_lock.release()