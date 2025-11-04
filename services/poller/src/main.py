from fastapi import FastAPI
import uvicorn
import httpx

from src.models import APIResponse
import time
import http

app = FastAPI()

PUNCTUATION = ('.', '!', '?')


def check_punctuation(fact: str) -> bool:
    return fact.endswith(PUNCTUATION)

def check_length(fact: str, expected_length: int) -> bool:
    return len(fact) == expected_length

@app.get("/")
async def main():
    async with httpx.AsyncClient() as client:
        start = time.monotonic()
        resp = await client.get("https://catfact.ninja/fact")
        latency = time.monotonic() - start

        resp_json = resp.json()
        fact = resp_json['fact']
        length = resp_json['length']

        return APIResponse(
            latency=latency,
            failed_request=resp.status_code != http.HTTPStatus.OK,
            length_correct=check_length(fact, length),
            punctuation=check_punctuation(fact),
        ).model_dump()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)