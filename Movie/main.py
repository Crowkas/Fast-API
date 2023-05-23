from fastapi import Depends, FastAPI, Body, Path, Query, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List
from jwt_manager import create_token, validate_token
from fastapi.security import HTTPBearer
from unidecode import unidecode


app = FastAPI()
app.title = 'Mi aplicación con FastAPI'
app.version = '0.0.1'


class JWTBearer(HTTPBearer):
    async def __call__(self, request : Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if data['email'] != 'admin@gmail.com':
            raise HTTPException(status_code = 403, detail = 'Credenciales son invalidas')

class User(BaseModel):
    email : str
    password : str

class Movie(BaseModel):
    id : Optional[int] = None
    title : str = Field(min_length = 5, max_length = 15)
    overview : str = Field(min_length = 15, max_length = 50)
    year : int = Field(le = 2022)
    rating : float = Field(ge = 1, le = 5.0)
    category : str = Field(min_length = 5, max_length = 10)

    class Config:
        schema_extra = {
            'example' : {
                'id' : 1,
                'title': 'Mi película',
                'overview' : 'Descripción de la película',
                'year' : 2022,
                'rating' : 5.0,
                'category' : 'Acción'
            }
        }

movies = [
    {
        'id': 1,
        'title': 'Avatar',
        'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        'year': 2009,
        'rating': 7.8,
        'category': 'Acción'  
    },
    {
        'id': 2,
        'title': 'Avatar',
        'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        'year': 2008,
        'rating': 7.8,
        'category': 'Drama'  
    }
]

@app.get('/', tags = ['home'])
def message():
    return HTMLResponse('<h1>Hello World</h1>')
    print(unidecode(category.capitalize()))

@app.post('/login', tags = ['auth'])
def login(user : User):
    if user.email == 'admin@gmail.com' and user.password == 'admin':
        token: str = create_token(user.dict())
    return JSONResponse(status_code = 200, content = token)

@app.get('/movies', tags = ['movies'], response_model = List[Movie], status_code = 200, dependencies = [Depends(JWTBearer())])
def get_movies() -> List[Movie]:
    return JSONResponse(status_code = 200, content = movies)

@app.get('/movies/{id}', tags = ['movies'], response_model = Movie)
def get_movie(id : int = Path(ge = 1, le =2000)) -> Movie:
    filtered_id = [i for i in movies if i['id'] == id]
    return JSONResponse(content = filtered_id[0]) if filtered_id else JSONResponse(status_code = 404, content = [])

@app.get('/movies/', tags = ['movies'], response_model = List[Movie])
def get_movies_by_category(category : str = Query(min_lenght = 5, max_length = 15), year : int = Query(ge = 1900, le = 2022))-> List[Movie]:
    cat = unidecode(category.capitalize())
    #For
    '''for i in movies:
        if unidecode(i['category']) == cat or i['year'] == year:
            return i
    return[]'''
    #High order function
    '''filtered_movies = list(filter(lambda i: unidecode(i['category']) == cat or i['year'] == year, movies))
    return filtered_movies'''
    #List comprehension
    filtered_movies = [i for i in movies if unidecode(i['category']) == cat or i['year'] == year]
    return JSONResponse(content = filtered_movies)

@app.post('/movies', tags = ['movies'], response_model = dict, status_code = 201)
def create_movies(movie : Movie) -> dict:
    movies.append(movie)
    return JSONResponse(status_code = 201, content = {'message' : 'Se ha registrado la película'})

@app.put('/movies/{id}', tags = ['movies'], response_model = dict, status_code = 200)
def update_movie(id : int, movie : Movie) -> dict:
    for i in movies:
        if i['id'] == id:
            i['title'] = movie.title
            i['overview'] = movie.overview
            i['year'] = movie.year
            i['rating'] = movie.rating
            i['category'] = movie.category
            return JSONResponse(status_code = 200, content = {'message' : 'Se ha modificado la película'})

@app.delete('/movies/{id}', tags = ['movies'], response_model = dict, status_code = 200)
def delete_movie(id : int) -> dict:
    for i in movies:
        if i['id'] == id:
            movies.remove(i)
            return JSONResponse(status_code = 200, content = {'message' : 'Se ha eliminado la película'})
