from src.enums.enums import player_status
from src.db.DBA import DBA
from src.db.translators import CourtTranslator

class CourtDBA(DBA):

    def __init__(self):
        self.COURTS_TABLE = 'Courts'
        self.ct = CourtTranslator()
        DBA.__init__(self)
    
    def get_courts(self):
        return [self.ct.fromDb(i) for i in self.client.scan(
            TableName=self.COURTS_TABLE
        )['Items']]
    
    def get_court(self, court_id):
        key={
            'id': court_id
        }
        court = self.client.get_item(
            TableName=self.COURTS_TABLE,
            Key=self.ct.toDB(key)
        )
        if ('Item' in court):
            return self.ct.fromDb(court['Item'])
        return None
    
    def clear_court(self, court_id):
        court = self.get_court(court_id)
        if court == None:
            return 'Failedto find court!'
        players = court['players'][:]
        court['occupied'] = False
        court['players'] = []
        
        self.client.put_item(
            TableName=self.COURTS_TABLE,
            Item=self.ct.toDB(court)
        )
        return players

    def put_on_court(self, court_id, players):
        court = self.get_court(court_id)
        if (court == None):
            return 'No such court!!'
        if (court['occupied'] == True):
            return 'Court is occupied!'
        court['occupied'] = True
        court['players'] = players

        self.client.put_item(
            TableName=self.COURTS_TABLE,
            Item=self.ct.toDB(court)
        )
        return court