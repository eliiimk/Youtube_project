import os
import requests
from dotenv import load_dotenv
from pymongo import MongoClient
from datetime import datetime

# Charger les variables d'environnement
load_dotenv(dotenv_path='config/.env')

API_KEY = os.getenv("API_KEY")
CHANNELS = os.getenv("CHANNELS")
MONGO_URI = os.getenv("MONGO_URI")

# Connexion MongoDB
client = MongoClient(MONGO_URI)
db = client["youtube_project"]
collection = db["videos"]

def get_channel_id_by_name(channel_name):
    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "key": API_KEY,
        "q": channel_name,
        "part": "snippet",
        "type": "channel",
        "maxResults": 1
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        items = response.json().get("items")
        if items:
            return items[0]["snippet"]["channelId"]
        else:
            print(f"⚠️ Aucun channel trouvé pour '{channel_name}'")
            return None
    else:
        print(f"❌ Erreur API {response.status_code} :", response.text)
        return None

def get_channel_videos(channel_id, max_results=50):
    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "key": API_KEY,
        "channelId": channel_id,
        "part": "snippet",
        "order": "date",
        "maxResults": max_results,
        "type": "video"
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        return response.json().get("items", [])
    else:
        print(f"❌ Erreur API {response.status_code} :", response.text)
        return []

def store_video(video):
    video_id = video["id"]["videoId"]
    title = video["snippet"]["title"]
    published_at = video["snippet"]["publishedAt"]
    channel_title = video["snippet"]["channelTitle"]

    if not collection.find_one({"video_id": video_id}):
        collection.insert_one({
            "video_id": video_id,
            "title": title,
            "published_at": datetime.strptime(published_at, "%Y-%m-%dT%H:%M:%SZ"),
            "channel_title": channel_title,
            "url": f"https://www.youtube.com/watch?v={video_id}"
        })
        print(f"✅ Ajouté : {title}")
    else:
        print(f"⏩ Déjà présent : {title}")

if __name__ == "__main__":
    if not CHANNELS:
        print("⚠️ La variable CHANNELS n'est pas définie dans .env")
    else:
        channel_names = [ch.strip() for ch in CHANNELS.split(",")]
        for name in channel_names:
            print(f"\n🔍 Traitement de : {name}")
            channel_id = get_channel_id_by_name(name)
            if channel_id:
                videos = get_channel_videos(channel_id, max_results=50)
                for video in videos:
                    store_video(video)
