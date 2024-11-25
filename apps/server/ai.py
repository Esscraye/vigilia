import os
import json
import subprocess
from fastapi import HTTPException

# Fonction pour analyser les logs
async def analyze_logs():
    log_file_path = os.path.join('logs', 'data2.log')  # Chemin vers le fichier logs
    if not os.path.exists(log_file_path):
        raise HTTPException(status_code=404, detail="Log file not found")

    with open(log_file_path, 'r') as file:
        logs = file.read()

        # Préparer le prompt pour Ollama
        prompt = f"""
    You are an Intrusion Detection System (IDS) that analyzes log files. 
    Please analyze the following logs and return a response in JSON format. 
    The response should contain the following elements:
    - "problem_detected": a boolean indicating whether there is a problem or not.
    - "problem_type": a string describing the type of problem detected (e.g., "malicious activity", "unauthorized access").
    - "suspicious_log_lines_count": the number of suspicious log lines detected.
    - "threat_summaries": a list of summaries of the detected threats.
    - "details": a list of all malicious log lines with their full content.

    Here is an example of the expected JSON format:
    {
        "problem_detected": true,
        "problem_type": "malicious activity",
        "suspicious_log_lines_count": 5,
        "threat_summaries": [
            "Multiple failed login attempts from the same IP address.",
            "Unauthorized access attempt to sensitive resources."
        ],
        "details": [
            "2023-10-01 12:00:00 - Failed login attempt from IP 192.168.1.1.",
            "2023-10-01 12:05:00 - Unauthorized access attempt to /admin.",
            "2023-10-01 12:10:00 - Failed login attempt from IP 192.168.1.1.",
            "2023-10-01 12:15:00 - Suspicious file access detected.",
            "2023-10-01 12:20:00 - Multiple failed login attempts from IP 192.168.1.1."
        ]
    }

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
        except json.JSONDecodeError as e:
            raise HTTPException(status_code=500, detail="Invalid JSON response") from e
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Exception: {str(e)}") from e

