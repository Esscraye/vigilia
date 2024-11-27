import os
import json
import requests
from fastapi import HTTPException
from pydantic import BaseModel

# Define the Query model
class Query(BaseModel):
    prompt: str
    model: str = "llama3.2"

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
                  "raw": True,
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
    query = Query(
        model="ollama/ollama-7b-v1",
        prompt=prompt,
    )

    try:
        # Send the request to Ollama
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": query.model,
                  "prompt": query.prompt,
                  "stream": False,
                  "raw": True,
                  "format": "json",
                  }
        )
        response.raise_for_status()  # Raise an error for bad responses

        response_json = response.json()
        print("response: ", response_json)
        return response_json
    except requests.RequestException as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error communicating with Ollama: {str(e)}",
        )    
