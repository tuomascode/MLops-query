import httpx

from src.modelsmodels import CatApiResponse, PollInstance
import time
import http


def check_punctuation(fact: str) -> bool:
    return fact.endswith(PUNCTUATION)


def check_length(fact: str, expected_length: int) -> bool:
    return len(fact) == expected_length


async def poll() -> PollInstance:
    async with httpx.AsyncClient() as client:
        start = time.monotonic()
        resp = await client.get(POLL_TARGET)
        latency = time.monotonic() - start

        resp_json = resp.json()
        fact = resp_json["fact"]
        length = resp_json["length"]

        ts = time.time()
        timestamp = (
            time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ts))
            + f".{int((ts - int(ts)) * 1000):03d}"
        )
        return PollInstance(
            timestamp=timestamp,
            latency=latency,
            failed_request=resp.status_code != http.HTTPStatus.OK,
            length_correct=check_length(fact, length),
            punctuation=check_punctuation(fact),
            api_response=CatApiResponse(fact=fact, length=length),
        )
