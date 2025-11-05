from functools import cache
import psycopg2

TABLE_NAME = "cat_api_data"

DB_NAME = "postgres"
DB_USERNAME = "postgres"
DB_HOST = "localhost"
DB_PORT = 12346
DB_PASS = "changeme"

@cache
def get_db_conn():
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USERNAME,
        host=DB_HOST,
        password=DB_PASS,
        port=DB_PORT,
    )
