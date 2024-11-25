from fastapi import FastAPI
from sse_starlette.sse import EventSourceResponse
from ai import analyze_logs
import time

app = FastAPI()

event_queue = []

results = {
  "timestamp": "string",
  "activity": "string",
  "risk_level": "Low",
  "details": "string"
}

@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/analyze-logs")
async def analyze_logs_endpoint():
    response = await analyze_logs()
    event = {"data": response}
    event_queue.append(event)
    return response


def data_streamer():
    while True:
        if event_queue:
            yield event_queue.pop(0)
        else:
            time.sleep(1)


@app.get('/notifications/sse')
async def main():
    return EventSourceResponse(data_streamer(), media_type='text/event-stream')

@app.post('/send-event')
async def send_event(event: str):
    event_queue.append('event')
    return {"message": "event sent"}

@app.get('/results')
async def get_results():
    return results