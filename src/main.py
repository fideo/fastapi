from fastapi import FastAPI, Depends, Query
from fastapi.requests import Request
from fastapi.responses import PlainTextResponse, Response, JSONResponse
from pydantic import BaseModel
from typing import Union, Annotated
from src.routers.movie_router import movie_router
from src.utils.http_error_handler import HTTPErrorHandler 
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os

def dependency1():
    print("Global dependency 1")

def dependency2():
    print("Global dependency 2")

app = FastAPI( dependencies = [Depends(dependency1), Depends(dependency2)] )

app.title = "Mi Primer Aplicación" # Cambio el titulo que muestra en /docs"
# app.version = "1.0.0" # Acá se le puede cambiar el número de versión por el que quiero

app.add_middleware(HTTPErrorHandler)
# @app.middleware('http')

static_path = os.path.join(os.path.dirname(__file__), 'static/') 
templates_path = os.path.join(os.path.dirname(__file__), 'templates/') 

app.mount('/static', StaticFiles(directory=static_path), 'static')
templates = Jinja2Templates(directory=templates_path)

async def http_error_handler(request: Request, call_next) -> Response | JSONResponse:
    print('Middleware is running!')
    return await call_next(request)

class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None

@app.get("/", tags=["Home"])
def home(request: Request):
    # return {"Hello": "World"}
    # return PlainTextResponse(content='Home', status_code=200)
    return templates.TemplateResponse('index.html', {'request': request, 'message': 'Welcome'})

# def common_param(start_date: str, end_date: str):
#   return { "start_date": start_date, "end_date": end_date }

# CommonDep = Annotated[dict, Depends(common_param)]

class CommonDep:
    def __init__(self, start_date: str, end_date: str) -> None:
        self.start_date = start_date
        self.end_date = end_date


@app.get("/users")
# def get_users(commons: CommonDep):
def get_users(commons: CommonDep = Depends(CommonDep)):
    # return f"Users created between {commons['start_date']} and {commons['end_date']}"
    return f"Users created between {commons.start_date} and {commons.end_date}"

@app.get("/customers")
# def get_customers(commons: CommonDep):
def get_customers(commons: CommonDep = Depends()):
    # return f"Users created between {commons['start_date']} and {commons['end_date']}"
    return f"Users created between {commons.start_date} and {commons.end_date}"

# movie
app.include_router(prefix='/movies', router=movie_router)
# Fin movie

@app.get("/items/{item_id}", tags=["Items"])
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}", tags=["Items"])
def update_item(item_id: int, item: Item):
    return {"item_name": item.price, "item_id": item_id}
