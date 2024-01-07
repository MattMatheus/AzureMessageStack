import requests


def GenerateUserMessageObject(messagestack):
    """Creates a new AzureMessage protobuf from random user data pulled from the URL and returns a message
    stack object."""
    url = "https://randomuser.me/api/"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
    else:
        print("Failed to retrieve data:", response.status_code)

    try:
        azuremessage = messagestack.azuremessage.add()
        azuremessage.sku = data["results"][0]["gender"]
        azuremessage.name = data["results"][0]["name"]["first"]
        azuremessage.subscription = data["results"][0]["name"]["first"]
        azuremessage.id = data["results"][0]["location"]["postcode"]
        azuremessage.reservation = data["results"][0]["login"]["salt"]

    except Exception:
        GenerateUserMessageObject(messagestack)

    return messagestack


def ConvertStackToDict(messageobj):
    """Converts an AzureMessageStack object into a python dict for insertion into the mongo db."""
    data_dict = {
        "name": messageobj.name,
        "id": messageobj.id,
        "subscription": messageobj.subscription,
        "sku": messageobj.sku,
        "reservation": messageobj.reservation,
    }
    return data_dict
