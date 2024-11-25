# Script de Détection d'Intrusion (IDS) sur un VPS

Ce projet montre comment configurer et exécuter un script de détection d'intrusion (IDS) sur un serveur privé virtuel (VPS). Le script analyse des journaux (logs) et produit un résultat au format JSON indiquant s'il y a un problème ou non.

---

## Prérequis
Avant de commencer, assurez-vous d'avoir :
- Un VPS avec un accès SSH.
- Python 3 installé sur le VPS.
- Les clés API nécessaires (par exemple, clé OpenAI), si applicable.
- Une connaissance de base des commandes SSH et de l'utilisation du terminal.

---

## Étapes pour le Déploiement

### 1. Connexion au VPS
Connectez-vous au VPS via SSH :
ssh utilisateur@ip_du_vps

### 2. Installer les logiciels requis
Mettez à jour la liste des paquets et installez Python :
sudo apt update
sudo apt install python3 python3-pip -y

Installez les bibliothèques Python nécessaires :
pip3 install openai python-dotenv

### 3. Transférer le script vers le VPS
Depuis votre machine locale, exécutez :
scp votre_script.py utilisateur@ip_du_vps:/chemin/vers/destination

### 4. Exécuter le script
Lancez le script manuellement :
python3 /chemin/vers/detection_intrusion.py
