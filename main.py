from fastapi import FastAPI, HTTPException, Query
from db_operations import (
    create_tables, create_store, read_stores, read_stores_by_actor, read_stores_by_genre, update_store, delete_store,
    create_availability, read_availability, update_availability, delete_availability,
    create_film, read_films, update_film, delete_film,
    create_film_actor, read_film_actors, update_film_actor, delete_film_actor, read_stores_by_film,
)
from models import (
    StoreCreate, Store, AvailabilityCreate, Availability,
    FilmCreate, Film, FilmActorCreate, FilmActor, StoreWithFilm
)
from typing import List, Optional

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    create_tables()

@app.post("/stores/", response_model=Store)
async def create_new_store(store: StoreCreate):
    try:
        store_id = create_store(store.store_name, store.location)
        created_store = Store(store_id=store_id, **store.dict())
        return created_store
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating store: {str(e)}")

@app.get("/stores/", response_model=List[Store])
async def get_all_stores():
    try:
        stores = read_stores()
        return [Store(store_id=store[0], store_name=store[1], location=store[2]) for store in stores]
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to retrieve stores")

@app.put("/stores/{store_id}", response_model=Store)
async def update_existing_store(store_id: int, store: StoreCreate):
    try:
        update_store(store_id, store.store_name, store.location)
        updated_store_data = read_stores()
        updated_store = next((Store(store_id=s[0], store_name=s[1], location=s[2]) for s in updated_store_data if s[0] == store_id), None)
        if updated_store:
            return updated_store
        else:
            raise HTTPException(status_code=404, detail=f"Store with ID {store_id} not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating store: {str(e)}")

@app.delete("/stores/{store_id}")
async def delete_existing_store(store_id: int):
    try:
        delete_store(store_id)
        return {"message": f"Store with ID {store_id} deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting store: {str(e)}")

@app.post("/availability/", response_model=Availability)
async def create_new_availability(availability: AvailabilityCreate):
    try:
        availability_id = create_availability(availability.store_id, availability.film_id)
        created_availability = Availability(availability_id=availability_id, **availability.dict())
        return created_availability
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating availability: {str(e)}")

@app.get("/availability/", response_model=List[Availability])
async def get_all_availability():
    try:
        availability = read_availability()
        return [Availability(availability_id=a[0], store_id=a[1], film_id=a[2]) for a in availability]
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to retrieve availability")

@app.put("/availability/{availability_id}", response_model=Availability)
async def update_existing_availability(availability_id: int, availability: AvailabilityCreate):
    try:
        update_availability(availability_id, availability.store_id, availability.film_id)
        updated_availability = Availability(availability_id=availability_id, store_id=availability.store_id, film_id=availability.film_id)
        return updated_availability
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating availability: {str(e)}")

@app.delete("/availability/{availability_id}")
async def delete_existing_availability(availability_id: int):
    try:
        delete_availability(availability_id)
        return {"message": f"Availability with ID {availability_id} deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting availability: {str(e)}")

@app.post("/films/", response_model=Film)
async def create_new_film(film: FilmCreate):
    try:
        film_id = create_film(film.title, film.release_year, film.genre)
        created_film = Film(film_id=film_id, **film.dict())
        return created_film
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating film: {str(e)}")

@app.get("/films/", response_model=List[Film])
async def get_all_films():
    try:
        films = read_films()
        return [Film(film_id=film[0], title=film[1], release_year=film[2], genre=film[3]) for film in films]
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to retrieve films")

@app.put("/films/{film_id}", response_model=Film)
async def update_existing_film(film_id: int, film: FilmCreate):
    try:
        update_film(film_id, film.title, film.release_year, film.genre)
        updated_film_data = read_films()
        updated_film = next((Film(film_id=f[0], title=f[1], release_year=f[2], genre=f[3]) for f in updated_film_data if f[0] == film_id), None)
        if updated_film:
            return updated_film
        else:
            raise HTTPException(status_code=404, detail=f"Film with ID {film_id} not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating film: {str(e)}")

@app.delete("/films/{film_id}")
async def delete_existing_film(film_id: int):
    try:
        delete_film(film_id)
        return {"message": f"Film with ID {film_id} deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting film: {str(e)}")

@app.post("/film_actors/", response_model=FilmActor)
async def create_new_film_actor(film_actor: FilmActorCreate):
    try:
        actor_id = create_film_actor(film_actor.film_id, film_actor.actor_name)
        created_film_actor = FilmActor(actor_id=actor_id, film_id=film_actor.film_id, actor_name=film_actor.actor_name)
        return created_film_actor
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating film actor: {str(e)}")

@app.get("/film_actors/", response_model=List[FilmActor])
async def get_all_film_actors():
    try:
        film_actors = read_film_actors()
        return [FilmActor(actor_id=actor[0], film_id=actor[1], actor_name=actor[2]) for actor in film_actors]
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to retrieve film actors")

@app.put("/film_actors/{actor_id}", response_model=FilmActor)
async def update_existing_film_actor(actor_id: int, film_actor: FilmActorCreate):
    try:
        update_film_actor(actor_id, film_actor.film_id, film_actor.actor_name)
        updated_film_actor = FilmActor(actor_id=actor_id, film_id=film_actor.film_id, actor_name=film_actor.actor_name)
        return updated_film_actor
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating film actor: {str(e)}")

@app.delete("/film_actors/{actor_id}")
async def delete_existing_film_actor(actor_id: int):
    try:
        delete_film_actor(actor_id)
        return {"message": f"Film actor with ID {actor_id} deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting film actor: {str(e)}")

@app.get("/stores/films", response_model=List[StoreWithFilm])
async def get_stores_by_search(
    film_name: Optional[str] = Query(None, description="Search by film name"),
    genre: Optional[str] = Query(None, description="Search by genre"),
    actor: Optional[str] = Query(None, description="Search by actor name")
):
    search_params = {"film_name": film_name, "genre": genre, "actor": actor}
    search_params = {k: v for k, v in search_params.items() if v is not None}

    if len(search_params) != 1:
        raise HTTPException(status_code=400, detail="Specify exactly one search parameter: film_name, genre, or actor")

    search_type, search_value = next(iter(search_params.items()))

    try:
        if search_type == "film_name":
            stores = read_stores_by_film(search_value)
        elif search_type == "genre":
            stores = read_stores_by_genre(search_value)
        elif search_type == "actor":
            stores = read_stores_by_actor(search_value)
        else:
            raise HTTPException(status_code=400, detail="Invalid search parameter")

        return [StoreWithFilm(store_id=store[0], store_name=store[1], location=store[2], film_name=store[3]) for store in stores]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching stores by {search_type}: {str(e)}")