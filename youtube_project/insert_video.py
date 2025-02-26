import pymongo
from dotenv import load_dotenv
import os
import certifi

# Charger les variables d'environnement
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://eliiimk:<29092231E&mk>@cluster0.qd63n.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

# Connexion à MongoDB avec certificat SSL et CA fourni par certifi
client = pymongo.MongoClient(MONGO_URI, ssl=True, tlsCAFile=certifi.where())
db = client["youtube_project"]
collection = db["videos"]

def insert_video(video_data):
    """Insère une vidéo dans la base de données"""
    collection.insert_one(video_data)
    print("Vidéo insérée avec succès !")

# Exemple de vidéo à insérer
video_example = {
    "video_id": "12345",
    "title": "Exemple de vidéo",
    "description": "Description de la vidéo.",
    "views": 1000,
    "published_at": "2025-02-25"
}

# Insérer la vidéo dans la base de données
insert_video(video_example)


