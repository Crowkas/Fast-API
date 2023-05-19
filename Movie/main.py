from fastapi import FastAPI, Body
from fastapi.responses import HTMLResponse
from unidecode import unidecode

app = FastAPI()
app.title = 'Mi aplicación con FastAPI'
app.version = '0.0.1'


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

@app.get('/movies', tags = ['movies'])
def get_movies():
    return movies

@app.get('/movies/{id}', tags = ['movies'])
def get_movie(id : int):
    filtered_id = [i for i in movies if i['id'] == id]
    return filtered_id

@app.get('/movies/', tags = ['movies'])
def get_movies_by_category(category : str, year : int):
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
    return filtered_movies

@app.post('/movies', tags = ['movies'])
def create_movies(id : int = Body(), title : str = Body(), overview : str = Body(), year : int = Body(), rating : float = Body(), category : str = Body()):
    movies.append({
        'id': id,
        'title': title,
        'overview': overview,
        'year': year,
        'rating': rating,
        'category': category
    })
    return movies

@app.put('/movies', tags = ['movies'])
def delete_movies(id : int):
    for i in movies:
        if i['id'] == id:
            movies.remove(i)
            break
    return movies
