import messagestack as ms
import azuremessage_pb2
import requests
from pymongo import MongoClient
import messagestack as ms

client = MongoClient('mongodb://localhost:27017/')
db = client['azuremessages']
collection = db['teststack']
messagestack = azuremessage_pb2.AzureMessageStack()

def GenerateUserMessageObject(messagestack):
    """Creates a new AzureMessage protobuf from random user data pulled from the URL and returns a message
       stack object."""
    url = 'https://randomuser.me/api/'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
    else:
        print("Failed to retrieve data:", response.status_code)

    azuremessage = messagestack.azuremessage.add()
    azuremessage.sku = data["results"][0]["gender"]
    azuremessage.name = data["results"][0]["name"]["first"]
    azuremessage.subscription = data["results"][0]["name"]["first"]
    azuremessage.id = data["results"][0]["location"]["postcode"]
    azuremessage.reservation = data["results"][0]["login"]["salt"]
    
    return messagestack

def ConvertStackToDict(messageobj):
    data_dict = {
        "name": messageobj.name,
        "id": messageobj.id,
        "subscription": messageobj.subscription,
        "sku": messageobj.sku,
        "reservation": messageobj.reservation
    }
    return data_dict

messageobj = GenerateUserMessageObject(messagestack)
for azuremessage in messageobj.azuremessage:
    dbmessage = ConvertStackToDict(azuremessage)
    collection.insert_one(dbmessage)