import threading
import time

class RefreshThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        # may or may not need this
        self.start_delay = 10
    
    def run(self):
        time.sleep(self.start_delay)
        