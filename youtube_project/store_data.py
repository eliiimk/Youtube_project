import pymongo
from fetch_data import fetch_youtube_data, get_channel_id  # Importation correcte
from dotenv import load_dotenv
import os
import certifi  # Ajout de certifi

# Charger les variables d'environnement
load_dotenv()

# Récupérer l'URI MongoDB depuis le fichier .env
MONGO_URI = os.getenv("MONGO_URI")
if not MONGO_URI:
    raise ValueError("❌ MONGO_URI n'est pas défini dans .env")

try:
    # Connexion à MongoDB avec certifi pour le certificat SSL
    client = pymongo.MongoClient(MONGO_URI, ssl=True, tlsCAFile=certifi.where())
    db = client["youtube_project"]
    collection = db["videos"]

    # Vérifier la connexion
    client.admin.command("ping")
    print("✅ Connexion réussie à MongoDB !")

except pymongo.errors.OperationFailure as e:
    print(f"❌ Erreur d'authentification : {e}")
    exit(1)
except pymongo.errors.ServerSelectionTimeoutError as e:
    print(f"❌ Impossible de se connecter à MongoDB : {e}")
    exit(1)

def store_data_in_mongodb():
    """Stocke les vidéos récupérées dans MongoDB"""
    channel_name = os.getenv("CHANNEL_ID")  # Utilisez le nom du canal ici (ex: "LeParisien")
    if not channel_name:
        print("❌ CHANNEL_ID n'est pas défini dans .env")
        return
    
    channel_id = get_channel_id(channel_name)
    if not channel_id:
        print(f"❌ Aucun ID trouvé pour le canal {channel_name}")
        return

    try:
        videos = fetch_youtube_data(channel_id)
        if not videos:
            print("⚠️ Aucune vidéo récupérée.")
            return

        for video in videos:
            video_data = {
                "video_id": video["id"].get("videoId", "N/A"),
                "title": video["snippet"]["title"],
                "description": video["snippet"]["description"],
                "publishedAt": video["snippet"]["publishedAt"],
                "channelTitle": video["snippet"]["channelTitle"]
            }

            # Utiliser upsert pour éviter des doublons sans appeler count_documents
            result = collection.update_one(
                {"video_id": video_data["video_id"]},
                {"$set": video_data},
                upsert=True
            )

            if result.upserted_id:
                print(f"✅ Vidéo {video_data['video_id']} insérée.")
            else:
                print(f"⚠️ Vidéo {video_data['video_id']} déjà présente.")

        print("✅ Toutes les vidéos ont été insérées avec succès !")
    
    except Exception as e:
        print(f"❌ Erreur lors de l'insertion des données : {e}")

if __name__ == "__main__":
    store_data_in_mongodb()
