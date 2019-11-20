
class TranslationError(Exception):
    def __init__(self, message):
        self.message = message

class Translator():
    def __init__(self, values, keys):
        self.values = values
        self.keys = keys
    
    def toDB(self, obj):
        item = {}
        for i in self.keys.keys():
            if i not in obj.keys():
                # translation error
                raise TranslationError("Translator toDb")
        for i in obj.keys():
            if (i in self.keys):
                item[i] = { self.keys[i]: obj[i] }
            if (i in self.values):
                if (self.values[i] == 'L'):
                    item[i] = { self.values[i]: [ {'S': j} for j in obj[i]] }
                else:
                    item[i] = { self.values[i]: obj[i] }
        return item
    
    def fromDb(self, item):
        obj = {}
        for i in self.keys.keys():
            if i not in item.keys():
                # translation error
                raise TranslationError("Translator fromDb")
        for i in item.keys():
            if (i in self.keys):
                obj[i] = item[i][self.keys[i]]
            if (i in self.values):
                if (self.values[i] == 'L'):
                    obj[i] = [j['S'] for j in item[i][self.values[i]]]
                else:
                    obj[i] = item[i][self.values[i]]
        return obj

class PlayerTranslator(Translator):
    def __init__(self):
        values = {
            'name':'S',
            'court':'S',
            'status': 'S',
            'queue-position':'N'
        }
        keys = {
            'id': 'S'
        }
        Translator.__init__(self, values, keys)

class QueueTranslator(Translator):
    def __init__(self):
        values = {
            'players': 'L'
        }
        keys = {
            'queue-name': 'S',
            'position': 'N'
        }
        Translator.__init__(self, values, keys)

class CourtTranslator(Translator):
    def __init__(self):
        values = {
            'name': 'S',
            'type': 'S',
            'players': 'L',
            'occupied': 'BOOL'
        }
        keys = {
            'id': 'S',
        }
        Translator.__init__(self, values, keys)