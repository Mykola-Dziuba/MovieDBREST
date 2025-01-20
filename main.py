from typing import List

from fastapi import Depends, FastAPI, HTTPException

import database
import schemas
import models
from database import db_state_default

app = FastAPI()
#
# async def reset_db_state():
#     database.db._state._state.set(db_state_default.copy())
#     database.db._state.reset()
#
#
# def get_db(db_state=Depends(reset_db_state)):
#     try:
#         database.db.connect()
#         yield
#     finally:
#         if not database.db.is_closed():
#             database.db.close()


# @app.get("/movies/", response_model=List[schemas.Movie], dependencies=[Depends(get_db)])
@app.get("/movies/", response_model=List[schemas.Movie])
def get_movies():
    return list(models.Movie.select())
    # movies = crud.get_movies()
    # return movies

# @app.get("/movies/", response_model=List[schemas.Movie], dependencies=[Depends(get_db)])
@app.post("/movies/", response_model=schemas.Movie)
def add_movie(movie: schemas.MovieBase):
    movie = models.Movie.create(**movie.dict())
    return movie

# @app.get(
#     "/movies/{movie_id}", response_model=schemas.Movie, dependencies=[Depends(get_db)]
# )
@app.get("/movies/{movie_id}", response_model=schemas.Movie)
def get_movie(movie_id: int):
    db_movie = models.Movie.filter(models.Movie.id == movie_id).first()
    if db_movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    return db_movie

@app.delete("/movies/{movie_id}", response_model=schemas.Movie)
def get_movie(movie_id: int):
    db_movie = models.Movie.filter(models.Movie.id == movie_id).first()
    if db_movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    db_movie.delete_instance()
    return db_movie
