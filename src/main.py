from fastapi import FastAPI, Body, Path, Query
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse, RedirectResponse, FileResponse
from pydantic import BaseModel, Field, validator
from typing import Optional, Union, List
from src.routers.movie_router import movie_router
import datetime

app = FastAPI()

app.title = "Mi Primer Aplicación" # Cambio el titulo que muestra en /docs"
# app.version = "1.0.0" # Acá se le puede cambiar el número de versión por el que quiero

class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None

@app.get("/", tags=["Home"])
def home():
    # return {"Hello": "World"}
    return PlainTextResponse(content='Home', status_code=200)

# movie
app.include_router(prefix='/movies', router=movie_router)
# Fin movie

@app.get("/items/{item_id}", tags=["Items"])
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}", tags=["Items"])
def update_item(item_id: int, item: Item):
    return {"item_name": item.price, "item_id": item_id}
