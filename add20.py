import uuid
from src.db.PlayerDBA import PlayerDBA
from src.db.QueueDBA import QueueDBA
from src.logic.player_logic import builder_player
from src.logic.queue_logic import logic_signup_group

users = []
names = []

qdba = QueueDBA()
pdba = PlayerDBA()

for i in range(20):
    users.append(chr(65+i) + '-user')
    names.append(chr(65+i) + '-name')
    if (pdba.get_player(users[i]) is None):
        pdba.put_player(builder_player(users[i], names[i]))

groups = []
for i in range(5):
    group = users[(i*4):((i+1)*4)]
    groups.append(group)

print(groups)

for i in groups:
    logic_signup_group(i)