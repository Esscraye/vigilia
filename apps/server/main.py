from typing import Union
from fastapi import FastAPI
from ai import analyze_logs

app = FastAPI()


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/analyze-logs")
async def analyze_logs_endpoint():
    response = await analyze_logs()
    return response