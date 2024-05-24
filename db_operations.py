import psycopg2
from config import DATABASE_CONFIG

class DatabaseError(Exception):
    pass

def get_db_connection():
    try:
        return psycopg2.connect(**DATABASE_CONFIG)
    except Exception as e:
        raise DatabaseError(f"Error connecting to PostgreSQL: {e}")

def execute_query(query, params=None, fetch=False):
    conn = get_db_connection()
    with conn.cursor() as cur:
        try:
            cur.execute(query, params)
            if fetch:
                results = cur.fetchall()
                conn.commit()
                return results
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise DatabaseError(f"Error executing query: {e}")
    conn.close()

def create_tables():
    conn = get_db_connection()
    with conn.cursor() as cur:
        try:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS film (
                    film_id SERIAL PRIMARY KEY,
                    title VARCHAR(255) NOT NULL,
                    release_year INT,
                    genre VARCHAR(50)
                );
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS film_actor (
                    actor_id SERIAL PRIMARY KEY,
                    film_id INT NOT NULL,
                    actor_name VARCHAR(255) NOT NULL,
                    FOREIGN KEY (film_id) REFERENCES film (film_id)
                );
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS store (
                    store_id SERIAL PRIMARY KEY,
                    store_name VARCHAR(255) NOT NULL,
                    location VARCHAR(255) NOT NULL
                );
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS availability (
                    availability_id SERIAL PRIMARY KEY,
                    store_id INT NOT NULL,
                    film_id INT NOT NULL,
                    FOREIGN KEY (store_id) REFERENCES store (store_id),
                    FOREIGN KEY (film_id) REFERENCES film (film_id)
                );
            """)
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise DatabaseError(f"Error creating tables: {e}")
    conn.close()


def create_film(title, release_year, genre):
    query = """
        INSERT INTO film (title, release_year, genre)
        VALUES (%s, %s, %s)
        RETURNING film_id;
    """
    params = (title, release_year, genre)
    return execute_query(query, params, fetch=True)[0][0]

def read_films():
    query = "SELECT * FROM film;"
    return execute_query(query, fetch=True)

def update_film(film_id, title, release_year, genre):
    query = """
        UPDATE film
        SET title = %s, release_year = %s, genre = %s
        WHERE film_id = %s;
    """
    params = (title, release_year, genre, film_id)
    execute_query(query, params)

def delete_film(film_id):
    query = "DELETE FROM film WHERE film_id = %s;"
    params = (film_id,)
    execute_query(query, params)

def create_film_actor(film_id, actor_name):
    query = """
        INSERT INTO film_actor (film_id, actor_name)
        VALUES (%s, %s)
        RETURNING actor_id;
    """
    params = (film_id, actor_name)
    return execute_query(query, params, fetch=True)[0][0]

def read_film_actors():
    query = "SELECT * FROM film_actor;"
    return execute_query(query, fetch=True)

def update_film_actor(actor_id, film_id, actor_name):
    query = """
        UPDATE film_actor
        SET film_id = %s, actor_name = %s
        WHERE actor_id = %s;
    """
    params = (film_id, actor_name, actor_id)
    execute_query(query, params)

def delete_film_actor(actor_id):
    query = "DELETE FROM film_actor WHERE actor_id = %s;"
    params = (actor_id,)
    execute_query(query, params)

def create_store(store_name, location):
    query = """
        INSERT INTO store (store_name, location)
        VALUES (%s, %s)
        RETURNING store_id;
    """
    params = (store_name, location)
    return execute_query(query, params, fetch=True)[0][0]

def read_stores():
    query = "SELECT * FROM store;"
    return execute_query(query, fetch=True)

def update_store(store_id, store_name, location):
    query = """
        UPDATE store
        SET store_name = %s, location = %s
        WHERE store_id = %s;
    """
    params = (store_name, location, store_id)
    execute_query(query, params)

def delete_store(store_id):
    query = "DELETE FROM store WHERE store_id = %s;"
    params = (store_id,)
    execute_query(query, params)

def create_availability(store_id, film_id):
    query = """
        INSERT INTO availability (store_id, film_id)
        VALUES (%s, %s)
        RETURNING availability_id;
    """
    params = (store_id, film_id)
    return execute_query(query, params, fetch=True)[0][0]

def read_availability():
    query = "SELECT * FROM availability;"
    return execute_query(query, fetch=True)

def update_availability(availability_id, store_id, film_id):
    query = """
        UPDATE availability
        SET store_id = %s, film_id = %s
        WHERE availability_id = %s;
    """
    params = (store_id, film_id, availability_id)
    execute_query(query, params)

def delete_availability(availability_id):
    query = "DELETE FROM availability WHERE availability_id = %s;"
    params = (availability_id,)
    execute_query(query, params)

def read_stores_by_film(film_name):
    query = """
        SELECT s.store_id, s.store_name, s.location, f.title
        FROM store s
        INNER JOIN availability a ON s.store_id = a.store_id
        INNER JOIN film f ON a.film_id = f.film_id
        WHERE f.title = %s;
    """
    params = (film_name,)
    return execute_query(query, params, fetch=True)

def read_stores_by_genre(genre):
    query = """
        SELECT s.store_id, s.store_name, s.location, f.title
        FROM store s
        INNER JOIN availability a ON s.store_id = a.store_id
        INNER JOIN film f ON a.film_id = f.film_id
        WHERE f.genre = %s;
    """
    params = (genre,)
    return execute_query(query, params, fetch=True)

def read_stores_by_actor(actor):
    query = """
        SELECT s.store_id, s.store_name, s.location, f.title
        FROM store s
        INNER JOIN availability a ON s.store_id = a.store_id
        INNER JOIN film_actor fa ON a.film_id = fa.film_id
        INNER JOIN film f ON fa.film_id = f.film_id
        WHERE fa.actor_name = %s;
    """
    params = (actor,)
    return execute_query(query, params, fetch=True)
