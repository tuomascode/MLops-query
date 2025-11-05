from fastapi import FastAPI
import uvicorn

from src.models import TimeseriesAPIResponse
from src.poller import poll
from src.db.conn import poll_instance_to_db, fetch_api_response
import asyncio

app = FastAPI()


async def _periodic_db_insert():
    while True:
        try:
            poll_instance = await poll()
            poll_instance_to_db(poll_instance)
        except Exception:
            # ignore errors or add logging here
            pass
        await asyncio.sleep(1)


@app.on_event("startup")
async def start_background_tasks():
    _prevent_gc = asyncio.create_task(_periodic_db_insert())


@app.get("/")
async def main() -> TimeseriesAPIResponse:
    return fetch_api_response()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
