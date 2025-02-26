import os
import requests
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()
API_KEY = os.getenv("API_KEY")
CHANNEL_NAME = os.getenv("CHANNEL_ID")  # Utilise le nom du canal (par exemple, LeParisien)

def get_channel_id(channel_name):
    """Récupère l'ID d'un canal YouTube à partir de son nom personnalisé"""
    url = f"https://www.googleapis.com/youtube/v3/search?key={API_KEY}&q={channel_name}&type=channel&part=snippet"
    response = requests.get(url)
    data = response.json()
    
    # Affiche la réponse complète pour déboguer
    print("Réponse de l'API pour l'ID du canal:", data)

    if "items" in data and len(data["items"]) > 0:
        return data["items"][0]["id"]["channelId"]
    else:
        return None

def fetch_youtube_data(channel_id):
    """Récupère les vidéos d'un channel YouTube via l'API"""
    url = f"https://www.googleapis.com/youtube/v3/search?key={API_KEY}&channelId={channel_id}&part=snippet&maxResults=10"
    response = requests.get(url)
    data = response.json()
    return data.get("items", [])

if __name__ == "__main__":
    # Récupérer l'ID du canal à partir du nom personnalisé
    channel_id = get_channel_id(CHANNEL_NAME)
    if channel_id:
        print(f"ID du canal : {channel_id}")
        # Récupérer les vidéos du canal
        videos = fetch_youtube_data(channel_id)
        print(videos)
    else:
        print("Le canal n'a pas été trouvé.")
