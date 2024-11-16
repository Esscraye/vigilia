import os
from dotenv import load_dotenv
from groq import Groq
import json

load_dotenv()

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY")
)

async def analyze_logs():
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
                "content": "Give me a name for your system (an IDS using AI to detect nulnerability)",  # Envoyer le contenu des logs
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
