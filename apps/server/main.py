from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi import HTTPException
from sse_starlette.sse import EventSourceResponse
from dotenv import load_dotenv
from groq import Groq
import requests
import time
import os
import json

load_dotenv()

app = FastAPI()

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY")
)

class Query(BaseModel):
    prompt: str
    model: str = "llama3.2"
event_queue = []

results = {
  "timestamp": "string",
  "activity": "string",
  "risk_level": "Low",
  "details": "string"
}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api")
async def read_root():
    return {"Hello": "World"}


@app.get("/api/analyze-logs-ollama")
async def analyze_logs_ollama_endpoint():
    response = await analyze_logs_with_ollama()
    event = {"data": response}
    event_queue.append(event)
    global results
    results = response
    await send_event('event')
    return response

@app.get("/api/analyze-logs-groq")
async def analyze_logs_ollama_endpoint():
    response = await analyze_logs_with_groq()
    event = {"data": response}
    event_queue.append(event)
    global results
    results = response
    await send_event('event')
    return response

def data_streamer():
    while True:
        if event_queue:
            yield event_queue.pop(0)
        else:
            time.sleep(1)


@app.get('/api/notifications/sse')
async def main():
    return EventSourceResponse(data_streamer(), media_type='text/event-stream')

@app.post('/api/send-event')
async def send_event(event: str):
    event_queue.append('event')
    return {"message": "event sent"}

@app.get('/api/results')
async def get_results():
    return results

# Function to analyze logs
async def analyze_logs_with_ollama():
    log_file_path = os.path.join('logs', 'data2.log')  # Path to the log file
    if not os.path.exists(log_file_path):
        raise HTTPException(status_code=404, detail="Log file not found")

    with open(log_file_path, 'r') as file:
        logs = file.read()

        # Prepare the prompt for Ollama
        prompt = f"""
You are an Intrusion Detection System (IDS) that analyzes log files. 
Please analyze return a response with the following information, and only theese informations:

-    problem_detected
-    problem_type
-    suspicious_log_lines_count
-    threat_summaries
-    details: [ 
        - each line is a log line
    ]

Logs you need to analyze:
{logs}
"""

    # Create a Query object
    query = Query(prompt=prompt)

    try:
        # Send the request to Ollama
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": query.model,
                  "prompt": query.prompt,
                  "stream": False,
                  "format": "json",
                  }
        )
        response.raise_for_status()  # Raise an error for bad responses

        # Get the generated text from the response
        generated_response = response.json()["response"]
        print(generated_response)
        # Load the JSON response
        try:
            response_json = json.loads(generated_response)
        except json.JSONDecodeError as e:
            raise HTTPException(status_code=500, detail="Invalid JSON response") from e

        return response_json
    except requests.RequestException as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error communicating with Ollama: {str(e)}",
        ) from e

async def analyze_logs_with_groq():
    log_file_path = os.path.join('logs', 'data.log')  # Remplacez par le nom de votre fichier log
    with open(log_file_path, 'r') as file:
        logs = file.read()
    
    # Préparer le message pour l'IA
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are an Intrusion Detection System (IDS) that analyzes log files. Please analyze the following logs and return a JSON response indicating whether there is a problem or not."
            },
            {
                "role": "user",
                "content": logs,  # Envoyer le contenu des logs
            }
        ],
        model="llama-3.1-70b-versatile",  # Modèle à utiliser
        stream=False,
    )

    response = chat_completion.choices[0].message.content  # Récupérer la réponse de l'IA
    if "```json" in response:
        response = response.split("```json")[1].split("```")[0]
    elif "```" in response:
        response = response.split("```")[1].split("```")[0]
    print(response)
    try:
        response = json.loads(response)
    except json.JSONDecodeError:
        print("JSONDecodeError")
        response = False
    return response  # Retourner la réponse de l'IA