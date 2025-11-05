from fastapi import FastAPI
import uvicorn

from src.models import PollInstance

app = FastAPI()

PUNCTUATION = (".", "!", "?")
POLL_TARGET = "https://catfact.ninja/fact"


@app.get("/")
async def main() -> PollInstance:
    return await poll()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
