from fastapi import FastAPI
import uvicorn
import random

app = FastAPI()

def get_fact():
    facts = [
        "Honey never spoils.",
        "Bananas are berries, but strawberries aren't.",
        "Octopuses have three hearts.",
        "There are more stars in the universe than grains of sand on Earth."
    ]
    return random.choice(facts)

@app.get("/")
async def read_root():
    return {"message": "Hello from FastAPI"}

@app.get("/fact")
async def read_fact():
    return {"fact": get_fact()}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)