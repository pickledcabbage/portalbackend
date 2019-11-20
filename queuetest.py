from src.db.dba import DBAccessor
from src.logic.player_logic import builder_player
from src.logic.queue_logic import logic_signup_group

dba = DBAccessor()

users = ['alex-user', 'bob-user', 'charlie-user', 'dexter-user']
names = ['ALEX', 'BOB', 'CHARLIE', 'DEXTER']

for i in range(4):
    if (dba.get_player(users[i]) is None):
        dba.create_player(builder_player(users[i], names[i]))

#print(logic_signup_group(users))
