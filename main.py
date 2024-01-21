from fastapi import FastAPI, Body, Path, Query
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse, RedirectResponse, FileResponse
from pydantic import BaseModel, Field, validator
from typing import Optional, Union, List
import datetime

app = FastAPI()

app.title = "Mi Primer Aplicación" # Cambio el titulo que muestra en /docs"
# app.version = "1.0.0" # Acá se le puede cambiar el número de versión por el que quiero


class Movie(BaseModel):
    id: int
    title: str
    overview: str
    year: int 
    rating: float
    category: str

class MovieCreate(BaseModel):
    id: int
    title: str
    overview: str = Field(min_length=5, max_length=50)
    year: int = Field(le=datetime.date.today().year, ge=1900) # le => Significa que tiene que ser menor o igual (less than or equal)
    rating: float = Field(ge=0, le=10)
    category: str = Field(min_length=2, max_length=20)

    model_config = {
        'json_schema_extra':  {
            'example': {
                'id': 1,
                'title': 'My Movie',
                'overview': 'Esta película trata de ....',
                'year': datetime.date.today().year,
                'rating': 0,
                'category': 'Categoría'
            }
        }
    }

    @validator('title')
    def validate_title(cls, value):
        if len(value) < 5:
            raise ValueError('Title file must have a minimun length of 5 characters')

        if len(value) > 15:
            raise ValueError('Title file must have a maximun length of 15 characters')
        return value

movies: List[Movie] = []

class MovieUpdate(BaseModel):
    title: str
    overview: str
    year: int 
    rating: float
    category: str

class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None


@app.get("/", tags=["Home"])
def home():
    # return {"Hello": "World"}
    return PlainTextResponse(content='Home', status_code=200)

@app.get("/movies", tags=["Movies"], status_code=200, response_description='Nos debería devolver una respuesta exitosa')
def get_movies() -> List[Movie]:
    content = [movie.model_dump() for movie in movies]
    return JSONResponse(content=content, status_code=200)

@app.get("/movies/{id}", tags=["Movies"])
def get_movie(id: int = Path(gt=0)) -> Movie | dict:
    for movie in movies:
        if movie.id == id:
            movie.model_dump()
            return JSONResponse(content=movie.model_dump(), status_code=200)
    return JSONResponse(content={}, status_code=404)

@app.get("/movies/", tags=["Movies"])
def get_movie_by_category(category: str = Query(min_length=5,max_length=20)) -> Movie | dict:
    for movie in movies:
        if movie.category == category:
            return JSONResponse(content=movie.model_dump(), status_code=200)
    return JSONResponse(content={}, status_code=404)

@app.post("/movies", tags=["Movies"])
def create_movie( movie: MovieCreate ) -> List[Movie]:
    movies.append(movie)
    content = [movie.model_dump() for movie in movies]
    return JSONResponse(content=content, status_code=201)
    # return RedirectResponse(url='/movies', status_code=303)

@app.put("/movies/{id}", tags=["Movies"])
def update_movie(id: int, movie: MovieUpdate) -> List[Movie]:
    for item in movies:
        if item.id == id:
            item.title = movie.title
            item.overview = movie.overview
            item.year = movie.year
            item.rating = movie.rating
            item.category = movie.category
    content = [movie.model_dump() for movie in movies]
    return JSONResponse(content=content, status_code=200)

@app.delete("/movies/{id}", tags=["Movies"])
def delete_movie(id: int) -> List[Movie]:
    for movie in movies:
        if movie.id == id:
            movies.remove(movie)
    content = [movie.model_dump() for movie in movies]
    return JSONResponse(content=content, status_code=200)

@app.get("/get_file", tags=["Movies"])
def get_file():
    return FileResponse('file.txt')

@app.get("/items/{item_id}", tags=["Items"])
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}", tags=["Items"])
def update_item(item_id: int, item: Item):
    return {"item_name": item.price, "item_id": item_id}
