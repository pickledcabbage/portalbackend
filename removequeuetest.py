from src.db.QueueDBA import QueueDBA
from src.logic.queue_logic import logic_remove_group

qdba = QueueDBA()

token = '1'
user = 'M-user'


print(qdba.queue_position('5'))
#logic_remove_group(user)

#print(qdba.pop_from_queue())