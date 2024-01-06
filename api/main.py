from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
from bson import json_util
from pymongo import MongoClient

app = FastAPI()
templates = Jinja2Templates(directory="templates")
client = MongoClient('mongodb://localhost:27017/')
db = client['azuremessages']
collection = db['teststack']

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
    
# This is to allow referencing the styles.css in our static directory
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")