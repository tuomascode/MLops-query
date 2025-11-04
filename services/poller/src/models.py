from pydantic import BaseModel


class CatApiResponse(BaseModel):
    fact: str
    length: int


class PollInstance(BaseModel):
    timestamp: str
    latency: float
    failed_request: bool
    length_correct: bool
    punctuation: bool
    api_response: CatApiResponse
