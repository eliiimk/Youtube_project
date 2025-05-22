# 📺 YouTube Data Dashboard avec MongoDB et Streamlit

Ce projet permet d’explorer et de visualiser des données YouTube stockées dans MongoDB via une interface interactive construite avec **Streamlit**.

## 📦 Fonctionnalités

- 🔌 Connexion sécurisée à une base de données MongoDB Atlas.
- 📊 Visualisation dynamique :
  - Nombre de vidéos par chaîne (barres).
  - Répartition des vidéos par chaîne (camembert).
  - Nombre de vidéos publiées par mois et semaine.
- 🔍 Filtres interactifs par chaîne.
- 📥 Téléchargement des données en CSV.
- 📋 Tableau de toutes les vidéos collectées.

## 🧰 Technologies utilisées

- Python
- MongoDB Atlas
- Streamlit
- Pandas
- Matplotlib
- Pymongo

## 📁 Structure du projet

youtube_project/
├── config/
│ └── .env # Fichier des variables d’environnement
├── fetch_data.py # Script pour récupérer les vidéos depuis l’API YouTube
├── visualisation_mongo.py # Interface Streamlit pour la visualisation
├── requirements.txt # Dépendances Python
└── README.md # Ce fichier


---

## ⚙️ Installation

**Cloner le dépôt** :

```bash
git clone https://github.com/elimk/youtube_project.git
cd youtube_project

**Créer un environnement virtuel:**

python -m venv venv
source venv/bin/activate  # ou venv\Scripts\activate sous Windows

**Installer les dépendances:**

pip install -r requirements.txt

**Créer le fichier .env dans le dossier config/ :**
# config/.env
API_KEY=VOTRE_CLE_YOUTUBE
CHANNEL_ID=UCxxxxxxx
MONGO_URI=mongodb+srv://<user>:<mdp>@cluster.mongodb.net/youtube_project?retryWrites=true&w=majority


