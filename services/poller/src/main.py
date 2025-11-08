from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from src.models import TimeseriesAPIResponse
from src.poller import poll
from src.db.conn import poll_instance_to_db, fetch_api_response
import asyncio

app = FastAPI()

# Allow your frontend (React at port 5173)
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,          # or ["*"] for all
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def _periodic_db_insert():
    while True:
        try:
            poll_instance = await poll()
            poll_instance_to_db(poll_instance)
        except Exception:
            # ignore errors or add logging here
            pass
        await asyncio.sleep(2)


@app.on_event("startup")
async def start_background_tasks():
    _prevent_gc = asyncio.create_task(_periodic_db_insert())


@app.get("/")
async def main() -> TimeseriesAPIResponse:
    return fetch_api_response()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
