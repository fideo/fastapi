from pydantic import BaseModel, Field, validator
import datetime 

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


class MovieUpdate(BaseModel):
    title: str
    overview: str
    year: int 
    rating: float
    category: str
