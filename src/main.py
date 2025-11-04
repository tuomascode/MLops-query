from fastapi import FastAPI
import uvicorn
import httpx

app = FastAPI()

@app.get("/")
async def read_root():
    async with httpx.AsyncClient() as client:
        resp = await client.get("https://catfact.ninja/fact")
        print(resp)
        resp.raise_for_status()
        return resp.json()

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)