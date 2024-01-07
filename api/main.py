from fastapi import FastAPI, Request, status, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse, RedirectResponse
from bson import json_util
from pymongo import MongoClient

import messagestack
import createstack
import azuremessage_pb2

app = FastAPI()
templates = Jinja2Templates(directory="templates")
client = MongoClient("mongodb://localhost:27017/")
db = client["azuremessages"]
collection = db["teststack"]


def get_data_from_db():
    data = list(collection.find({}))
    return data


@app.get("/")
async def read_root(request: Request):
    data = get_data_from_db()
    return templates.TemplateResponse("table.html", {"request": request, "data": data})


@app.get("/raw")
async def return_raw():
    data = get_data_from_db()
    json_compatible_data = json_util.dumps(data)
    return JSONResponse(content=json_compatible_data)


@app.get("/create")
async def create_dbentry():
    messagestack = azuremessage_pb2.AzureMessageStack()
    messageobj = createstack.GenerateUserMessageObject(messagestack)
    for azuremessage in messageobj.azuremessage:
        dbmessage = createstack.ConvertStackToDict(azuremessage)
        collection.insert_one(dbmessage)
    return status.HTTP_201_CREATED


@app.post("/createmany")
async def create_item(count: int = 1):
    if count < 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Repeat count must be at least 1.",
        )
    try:
        for _ in range(count):
            messagestack = azuremessage_pb2.AzureMessageStack()
            messageobj = createstack.GenerateUserMessageObject(messagestack)
            for azuremessage in messageobj.azuremessage:
                dbmessage = createstack.ConvertStackToDict(azuremessage)
                collection.insert_one(dbmessage)
        return {
            "message": f"Item created successfully {count} times"
        }, status.HTTP_202_ACCEPTED
    except Exception as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@app.get("/reset")
async def reset_db():
    collection.delete_many({})
    response = RedirectResponse(url="/")
    return response


@app.post("/purgezeros")
async def purge_zeros():
    collection.delete_many({"id": 0})
    return status.HTTP_202_ACCEPTED


# This is to allow referencing the styles.css in our static directory
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
