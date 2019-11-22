# run this before importing boto3 to set proper time
import os
os.environ["TZ"] = "UTC"

from qtd import QTD
from ptd import PTD
from ctd import CTD
from createdb import CREATE_DB
from createcourts import CREATE_COURTS
from src.db.QueueDBA import QueueDBA
from src.db.PlayerDBA import PlayerDBA
from src.logic.player_logic import builder_player

def CREATE_20_PLAYERS():
    users = []
    names = []

    qdba = QueueDBA()
    pdba = PlayerDBA()

    for i in range(20):
        users.append(chr(65+i) + '-user')
        names.append(chr(65+i) + '-name')
        if (pdba.get_player(users[i]) is None):
            pdba.put_player(builder_player(users[i], names[i]))

if __name__ == "__main__":
    CREATE_DB()
    CREATE_COURTS()
    CREATE_20_PLAYERS()