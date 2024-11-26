import os
import json
import subprocess
from fastapi import HTTPException

# Fonction pour analyser les logs
async def analyze_logs():
    log_file_path = os.path.join('logs', 'data3.log')  # Chemin vers le fichier logs
    if not os.path.exists(log_file_path):
        raise HTTPException(status_code=404, detail="Log file not found")

    with open(log_file_path, 'r') as file:
        logs = file.read()
    
        # Préparer le prompt pour Ollama
    prompt = f"""
    You are an Intrusion Detection System (IDS) that analyzes log files. 
    Please analyze the following logs and return a JSON response indicating whether there is a malicious events or not. 
    In the output please identify : is_malicious_event_detected, number of malicious event detected, most frequently malicious event detected

    Structure of the JSON output : 
        is_malicious_event_detected: string,
        number_of_malicious_events_detected: string,
        most_frequent_malicious_event: 
            event_type: string,
            source_ip: ip address,
            destination_ip: ip address,
            message: string
    Logs:
    {logs}
    """

    try:
        # Appeler Ollama en local avec un pipe (stdin)
        result = subprocess.run(
            ["ollama", "run", "llama3.2"],
            input=prompt,
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            raise HTTPException(status_code=500, detail=f"Error from Ollama: {result.stderr}")

        response = result.stdout.strip()

        # Extraire la partie JSON si elle est entourée de ```json ou ```
        if "```json" in response:
            response = response.split("```json")[1].split("```")[0]
        elif "```" in response:
            response = response.split("```")[1].split("```")[0]

        # Charger la réponse JSON
        try:
            response = json.loads(response)
        except json.JSONDecodeError:
            raise HTTPException(status_code=500, detail="Invalid JSON response")
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Exception: {str(e)}")

