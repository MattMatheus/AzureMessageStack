from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
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

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")