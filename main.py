from typing import List
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import database
import schemas
import models
from database import db_state_default

app = FastAPI()

# Add CORS middleware to allow requests from React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, DELETE, etc.)
    allow_headers=["*"],  # Allow all headers
)


@app.get("/")
def read_root():
    return {"message": "API is running. Check /movies/ and /actors/ for data."}


# Movies Endpoints


@app.get("/movies/", response_model=List[schemas.Movie])
def get_movies():
    """Fetch all movies."""
    return list(models.Movie.select())


@app.post("/movies/", response_model=schemas.Movie)
def add_movie(movie: schemas.MovieBase):
    """Add a new movie to the database."""
    movie = models.Movie.create(**movie.dict())
    return movie


@app.get("/movies/{movie_id}", response_model=schemas.Movie)
def get_movie(movie_id: int):
    """Fetch a single movie by ID."""
    db_movie = models.Movie.filter(models.Movie.id == movie_id).first()
    if db_movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    return db_movie


@app.put("/movies/{movie_id}", response_model=schemas.Movie)
def update_movie(movie_id: int, movie: schemas.MovieBase):
    """Update an existing movie by ID, including actors."""
    db_movie = models.Movie.filter(models.Movie.id == movie_id).first()
    if db_movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")

    db_movie.title = movie.title
    db_movie.year = movie.year
    db_movie.director = movie.director
    db_movie.description = movie.description
    db_movie.save()

    # ✅ Обновляем связи с актерами
    db_movie.actors.clear()  # Удаляем всех текущих актеров
    if movie.actors:  # Добавляем новых актеров
        actors_to_add = models.Actor.select().where(models.Actor.id.in_(movie.actors))
        for actor in actors_to_add:
            db_movie.actors.add(actor)

    return db_movie


@app.delete("/movies/{movie_id}", response_model=schemas.Movie)
def delete_movie(movie_id: int):
    """Delete a movie by ID."""
    db_movie = models.Movie.filter(models.Movie.id == movie_id).first()
    if db_movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    db_movie.delete_instance()
    return db_movie


# Actors Endpoints


@app.get("/actors/", response_model=List[schemas.Actor])
def get_actors():
    """Fetch all actors."""
    actors = models.Actor.select()
    return [
        {"id": actor.id, "name": actor.name, "surname": actor.surname}
        for actor in actors
    ]


@app.get("/actors/{actor_id}", response_model=schemas.Actor)
def get_actor(actor_id: int):
    """Fetch a single actor by ID."""
    db_actor = models.Actor.filter(models.Actor.id == actor_id).first()
    if db_actor is None:
        raise HTTPException(status_code=404, detail="Actor not found")
    return {
        "id": db_actor.id,
        "name": db_actor.name,
        "surname": db_actor.surname,
    }


@app.post("/actors/", response_model=schemas.Actor)
def add_actor(actor: schemas.ActorCreate):
    """Add a new actor to the database."""
    new_actor = models.Actor.create(**actor.dict())
    return {"id": new_actor.id, "name": new_actor.name, "surname": new_actor.surname}


@app.delete("/actors/{actor_id}", response_model=schemas.Actor)
def delete_actor(actor_id: int):
    """Delete an actor by ID."""
    db_actor = models.Actor.filter(models.Actor.id == actor_id).first()
    if db_actor is None:
        raise HTTPException(status_code=404, detail="Actor not found")
    db_actor.delete_instance()
    return {"id": db_actor.id, "name": db_actor.name, "surname": db_actor.surname}


@app.post("/movies/{movie_id}/actors", response_model=schemas.Actor)
def add_actor_to_movie(movie_id: int, actor_id: int):
    """Link an actor to a movie."""
    db_movie = models.Movie.filter(models.Movie.id == movie_id).first()
    if db_movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")

    db_actor = models.Actor.filter(models.Actor.id == actor_id).first()
    if db_actor is None:
        raise HTTPException(status_code=404, detail="Actor not found")

    db_movie.actors.add(db_actor)
    return {"id": db_actor.id, "name": db_actor.name, "surname": db_actor.surname}
