from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import PlainTextResponse, Response, JSONResponse
from pydantic import BaseModel
from typing import Union
from src.routers.movie_router import movie_router
from src.utils.http_error_handler import HTTPErrorHandler 
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os

app = FastAPI()

app.title = "Mi Primer Aplicación" # Cambio el titulo que muestra en /docs"
# app.version = "1.0.0" # Acá se le puede cambiar el número de versión por el que quiero

# app.add_middleware(HTTPErrorHandler)
@app.middleware('http')

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
def home():
    # return {"Hello": "World"}
    # return PlainTextResponse(content='Home', status_code=200)
    return templates.TemplateResponse('index.html', {'message', 'Welcome'})

# movie
app.include_router(prefix='/movies', router=movie_router)
# Fin movie

@app.get("/items/{item_id}", tags=["Items"])
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}", tags=["Items"])
def update_item(item_id: int, item: Item):
    return {"item_name": item.price, "item_id": item_id}
