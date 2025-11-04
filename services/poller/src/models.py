from pydantic import BaseModel


class APIResponse(BaseModel):
    latency: float
    failed_request: bool
    length_correct: bool
    punctuation: bool
