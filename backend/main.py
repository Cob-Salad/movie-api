import uuid

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from schemas import (
    Movie,
    CreateMovieRequest,
    CreateMovieResponse,
    UpdateMovieRequest,
    UpdateMovieResponse,
    DeleteMovieResponse,
)


movies: list[Movie] = [
    Movie(movie_id=uuid.uuid4(), name="Spider-Man", year=2002),
    Movie(movie_id=uuid.uuid4(), name="Thor: Ragnarok", year=2017),
    Movie(movie_id=uuid.uuid4(), name="Iron Man", year=2008),
]


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/movies")
async def get_movies() -> list[Movie]:
    return movies

@app.post("/movies")
async def create_movie(movie_info: CreateMovieRequest) -> CreateMovieResponse:
    movie_id = uuid.uuid4()
    new_movie = Movie(
        name=movie_info.name,
        year=movie_info.year,
        movie_id=movie_id
    )

    movies.append(new_movie)
    return CreateMovieResponse(id=movie_id)

@app.put("/movies/{movie_id}")
async def update_movie(movie_id: uuid.UUID, updated_movie: UpdateMovieRequest) -> UpdateMovieResponse:
    id_list = []
    for i in movies:
        id_list.append(i.movie_id)

    if movie_id not in id_list:
        return UpdateMovieResponse(success=False)


    for index, movie in enumerate(movies):
        if movie.movie_id == movie_id:
            movies[index] = Movie(
                name=updated_movie.name,
                year=updated_movie.year,
                movie_id=movie_id
            )
            return UpdateMovieResponse(success=True)
    

@app.delete("/movies/{movie_id}")
async def delete_movie(movie_id: uuid.UUID) -> DeleteMovieResponse:
    id_list = []
    for i in movies:
        id_list.append(i.movie_id)

    if movie_id not in id_list:
        return DeleteMovieResponse(success=False)
    
    for index, movie in enumerate(movies):
        if movie.movie_id == movie_id:
            movies.pop(index)
            return DeleteMovieResponse(success=True)
