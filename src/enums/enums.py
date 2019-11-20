from enum import Enum

class player_status(Enum):
    ON_COURT = "ON_COURT"
    IDLE = "IDLE"
    IN_QUEUE = "IN_QUEUE"

    def __str__(self):
        return self.value