from functools import cache
from sqlalchemy import create_engine

TABLE_NAME = "cat_api_data"

DB_NAME = "postgres"
DB_USERNAME = "postgres"
DB_HOST = "localhost"
DB_PORT = 12346
DB_PASS = "changeme"


@cache
def get_db_conn():
    engine = create_engine(
        f"postgresql+psycopg2://{DB_USERNAME}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
    return engine.connect()
