import pymongo
from dotenv import load_dotenv
import os

# Charger les variables d'environnement
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://eliiimk:<29092231E&mk>@cluster0.qd63n.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

# Connexion à MongoDB
try:
    client = pymongo.MongoClient(MONGO_URI)
    print("Connexion réussie à MongoDB")
    db = client["youtube_project"]
    collection = db["videos"]
except Exception as e:
    print(f"Erreur de connexion à MongoDB: {e}")
    exit()

def clean_data():
    """Supprime les vidéos sans ID ou avec une description vide"""
    # Compte les vidéos concernées avant la suppression
    count_no_id = collection.count_documents({"video_id": "N/A"})
    count_empty_desc = collection.count_documents({"description": {"$eq": ""}})
    
    print(f"Vidéos sans ID : {count_no_id}, Vidéos avec description vide : {count_empty_desc}")

    # Suppression des vidéos sans ID ou avec une description vide en une seule requête
    result = collection.delete_many({
        "$or": [
            {"video_id": "N/A"},
            {"description": {"$eq": ""}}
        ]
    })

    print(f"Vidéos supprimées : {result.deleted_count}")

    # Compte les vidéos après la suppression
    count_after = collection.count_documents({})
    print(f"Nombre de vidéos restantes après suppression : {count_after}")
    print("Vidéos sans ID et avec description vide supprimées !")

# Appel de la fonction de nettoyage
clean_data()

