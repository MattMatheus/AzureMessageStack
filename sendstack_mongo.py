from pymongo import MongoClient
import messagestack as ms

client = MongoClient('mongodb://localhost:27017/')
db = client['azuremessages']
collection = db['teststack']

def ConvertStackToDict(messageobj):
    data_dict = {
        "name": messageobj.name,
        "id": messageobj.id,
        "subscription": messageobj.subscription,
        "sku": messageobj.sku,
        "reservation": messageobj.reservation
    }
    return data_dict

messageobj = ms.ReadMessageStack()

for azuremessage in messageobj.azuremessage:
    dbmessage = ConvertStackToDict(azuremessage)
    collection.insert_one(dbmessage)
