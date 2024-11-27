# Script de Détection d'Intrusion (IDS) sur un VPS

Ce projet montre comment configurer et exécuter un script de détection d'intrusion (IDS) sur un serveur privé virtuel (VPS). Le script analyse des journaux (logs) et produit un résultat au format JSON indiquant s'il y a un problème ou non.

---

## Services Inclus

Ce dépôt contient les éléments suivants :

- **Service Web** : Une application Next.js située dans le dossier `apps/web`.
- **Application API** : Une application FastAPI située dans le dossier `apps/server`, que vous pouvez lancer avec la commande :
  
  ```bash
  # Créer un environnement virtuel
  python -m venv venv
  # Activer l'environnement virtuel (Windows)
  venv\Scripts\activate
  # Activer l'environnement virtuel (macOS/Linux)
  source venv/bin/activate
  # Installer les dépendances
  pip install -r requirements.txt
  # Lancer l'application FastAPI
  fastapi dev main.py
  ```

### Configuration des Environnements

1. Dans le dossier `apps/server`, créez le fichier `.env` à partir de `.env.example`.
2. Dans le dossier `apps/web`, créez un fichier `.env.local` avec la ligne suivante :

   ```plaintext
   NEXT_PUBLIC_API_URL=http://localhost:8000/api
   ```
