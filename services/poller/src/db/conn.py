from functools import cache
from typing import Any
from sqlalchemy import create_engine

from src.models import PollInstance, TimeseriesAPIObject
from src.db.models import PollInstance as DBPollInstance
from sqlalchemy import insert
from sqlalchemy import select
from src.models import TimeseriesAPIResponse, CatApiResponse
import os

DB_HOST = os.getenv("POSTGRES_HOST", "localhost")
DB_PORT = os.getenv("POSTGRES_PORT", "12346")
DB_NAME = os.getenv("POSTGRES_DB", "postgres")
DB_USERNAME = os.getenv("POSTGRES_USER", "postgres")
DB_PASS = os.getenv("POSTGRES_PASSWORD", "changeme")

API_LIMIT = 10**5


@cache
def get_db_conn() -> Any:
    engine = create_engine(
        f"postgresql+psycopg2://{DB_USERNAME}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
    return engine.connect()


def poll_instance_to_db(poll_instance: PollInstance):
    conn = get_db_conn()
    stmt = insert(DBPollInstance).values(
        timestamp=poll_instance.timestamp,
        latency=poll_instance.latency,
        failed_request=poll_instance.failed_request,
        length_correct=poll_instance.length_correct,
        punctuation=poll_instance.punctuation,
        api_fact=poll_instance.api_response.fact,
        api_length=poll_instance.api_response.length,
    )
    conn.execute(stmt)
    conn.commit()


def fetch_api_response() -> TimeseriesAPIResponse:
    conn = get_db_conn()
    stmt = select(DBPollInstance).order_by(DBPollInstance.timestamp.asc()).limit(API_LIMIT)
    rows = conn.execute(stmt).mappings().all()

    instances = []
    for row in rows:
        api_response = CatApiResponse(fact=row["api_fact"], length=row["api_length"])
        instances.append(
            TimeseriesAPIObject(
                timestamp=row["timestamp"],
                latency=row["latency"],
                failed_request=row["failed_request"],
                length_correct=row["length_correct"],
                punctuation=row["punctuation"],
                api_response=api_response,
            )
        )

    return TimeseriesAPIResponse(response=instances)
