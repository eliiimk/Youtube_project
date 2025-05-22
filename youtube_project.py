import os
import pymongo
import certifi
from dotenv import load_dotenv
import pandas as pd
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

load_dotenv(dotenv_path=os.path.join('config', '.env'))

API_KEY = os.getenv("API_KEY")
CHANNELS = os.getenv("CHANNELS").split(",")
MONGO_URI = os.getenv("MONGO_URI")

if not MONGO_URI:
    raise ValueError("❌ MONGO_URI n'est pas défini dans .env")

class MongoDBClient:
    def __init__(self, uri, db_name):
        self.client = pymongo.MongoClient(uri, ssl=True, tlsCAFile=certifi.where())
        self.db = self.client[db_name]
        self._ensure_indexes()

    def _ensure_indexes(self):
        collection = self.db["videos"]
        # Index unique sur video_id pour éviter doublons
        collection.create_index("video_id", unique=True)
    
    def insert_data(self, collection_name, data):
        collection = self.db[collection_name]
        inserted_count = 0
        for doc in data:
            try:
                collection.insert_one(doc)
                inserted_count += 1
            except pymongo.errors.DuplicateKeyError:
                # Vidéo déjà insérée, on ignore
                pass
        print(f"✅ {inserted_count} nouveaux documents insérés.")
        return inserted_count

    def fetch_data(self, collection_name, query=None):
        collection = self.db[collection_name]
        return list(collection.find(query))

class YouTubeAPIClient:
    def __init__(self, api_key, youtube_version="v3"):
        self.youtube = build('youtube', youtube_version, developerKey=api_key)

    def get_channel_id(self, channel_name):
        try:
            request = self.youtube.search().list(
                q=channel_name,
                type='channel',
                part='snippet',
                maxResults=1
            )
            response = request.execute()
            items = response.get('items', [])
            if items:
                return items[0]['snippet']['channelId']
            else:
                print(f"❌ Aucune ID trouvée pour la chaîne '{channel_name}'.")
                return None
        except HttpError as e:
            print(f"❌ Erreur API YouTube lors de la recherche de chaîne : {e}")
            return None

    def get_channel_videos(self, channel_id, max_results=100):
        videos = []
        try:
            request = self.youtube.search().list(
                part="snippet",
                channelId=channel_id,
                maxResults=50,
                order="date",
                type="video"
            )
            response = request.execute()
            videos.extend(response.get('items', []))

            # Pagination
            while "nextPageToken" in response and len(videos) < max_results:
                next_page_token = response['nextPageToken']
                request = self.youtube.search().list(
                    part="snippet",
                    channelId=channel_id,
                    maxResults=50,
                    order="date",
                    type="video",
                    pageToken=next_page_token
                )
                response = request.execute()
                videos.extend(response.get('items', []))
                if len(videos) >= max_results:
                    break

            # Limiter à max_results
            return videos[:max_results]
        except HttpError as e:
            print(f"❌ Erreur API YouTube lors de la récupération des vidéos : {e}")
            return []

class VideoProcessor:
    def __init__(self, data):
        self.data = data

    def clean_data(self):
        cleaned = []
        for video in self.data:
            video_id = video.get('id', {}).get('videoId')
            description = video.get('snippet', {}).get('description', '')
            if video_id and description.strip():
                # Construire dict simplifié pour MongoDB
                cleaned.append({
                    "video_id": video_id,
                    "channelTitle": video['snippet'].get('channelTitle', ''),
                    "description": description,
                    "publishedAt": video['snippet'].get('publishedAt', ''),
                    "title": video['snippet'].get('title', '')
                })
        print(f"✅ Vidéos nettoyées : {len(cleaned)} vidéos valides.")
        return cleaned

    def to_dataframe(self):
        return pd.DataFrame(self.data)

class YouTubeDataPipeline:
    def __init__(self, mongo_uri, db_name, api_key):
        self.mongo_client = MongoDBClient(mongo_uri, db_name)
        self.youtube_client = YouTubeAPIClient(api_key)

    def fetch_and_store_data(self, channel_name):
        print(f"\n📺 Traitement de la chaîne : {channel_name}")
        channel_id = self.youtube_client.get_channel_id(channel_name)
        if not channel_id:
            print(f"❌ Impossible de récupérer l'ID du canal {channel_name}")
            return

        videos_raw = self.youtube_client.get_channel_videos(channel_id)
        processor = VideoProcessor(videos_raw)
        cleaned_videos = processor.clean_data()
        self.mongo_client.insert_data("videos", cleaned_videos)

    def explore_data(self):
        videos = self.mongo_client.fetch_data("videos")
        df = pd.DataFrame(videos)
        if df.empty:
            print("⚠️ Aucune donnée trouvée dans la base.")
            return

        print("\nAperçu des données :")
        print(df.head())

        if 'publishedAt' in df.columns:
            df['publishedAt'] = pd.to_datetime(df['publishedAt'], errors='coerce')
            print("\nStatistiques sur les dates de publication :")
            print(df['publishedAt'].describe())

        print("\nVidéos les plus récentes :")
        print(df.sort_values(by='publishedAt', ascending=False).head())

def clean_database(mongo_uri):
    client = MongoDBClient(mongo_uri, "youtube_project")
    collection = client.db["videos"]
    # Supprimer les vidéos sans video_id ou description vide
    result = collection.delete_many({
        "$or": [
            {"video_id": {"$exists": False}},
            {"description": {"$eq": ""}}
        ]
    })
    print(f"🧹 {result.deleted_count} vidéos supprimées de la base.")

if __name__ == "__main__":
    pipeline = YouTubeDataPipeline(MONGO_URI, "youtube_project", API_KEY)

    for channel_name in CHANNELS:
        pipeline.fetch_and_store_data(channel_name)

    clean_database(MONGO_URI)
    pipeline.explore_data()

