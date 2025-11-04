from fastapi import FastAPI
import uvicorn
import httpx

from src.models import APIResponse

app = FastAPI()

PUNCTUATION = ('.', '!', '?')


def check_punctuation(fact: str) -> bool:
    return fact.endswith(PUNCTUATION)

def check_length(fact: str, expected_length: int) -> bool:
    return len(fact) == expected_length

@app.get("/")
async def main():
    async with httpx.AsyncClient() as client:
        resp = await client.get("https://catfact.ninja/fact")
        resp.raise_for_status()

        resp_json = resp.json()
        fact = resp_json['fact']
        length = resp_json['length']
        return APIResponse(
            latency=0,
            failed_request=True,
            length_correct=check_length(fact, length),
            punctuation=check_punctuation(fact),
        ).model_dump_json()

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)