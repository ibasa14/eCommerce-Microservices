from psycopg2 import pool

class ConectionPool()
    connection_pool = psycopg2.pool.SimpleConnectionPool(
        1, 20,  # min and max number of connections
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        host=POSTGRES_HOST,
        port=POSTGRES_PORT,
        database=POSTGRES_DB
    )
