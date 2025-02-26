import pymongo
import pandas as pd
from dotenv import load_dotenv
import os

# Charger les variables d'environnement
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://eliiimk:<29092231E&mk>@cluster0.qd63n.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

# Connexion à MongoDB
client = pymongo.MongoClient(MONGO_URI)
db = client["youtube_project"]
collection = db["videos"]

def explore_data():
    """Explore les données stockées dans MongoDB avec Pandas"""
    videos = list(collection.find({}, {"_id": 0}))  # Récupère toutes les vidéos sans le champ _id
    df = pd.DataFrame(videos)
    
    print("Aperçu des données :")
    print(df.head())

    # Affichage des types de données
    print("\nTypes de données :")
    print(df.dtypes)

    print("\nValeurs manquantes :")
    print(df.isnull().sum())
    
    # Analyse des dates de publication
    if 'publishedAt' in df.columns:
        df['publishedAt'] = pd.to_datetime(df['publishedAt'], errors='coerce')
        print("\nStatistiques sur les dates de publication :")
        print(df['publishedAt'].describe())
        print("\nValeurs invalides dans 'publishedAt' :")
        print(df[df['publishedAt'].isnull()])
    
    # Affichage des vidéos les plus récentes
    print("\nVidéos les plus récentes :")
    print(df.sort_values(by='publishedAt', ascending=False).head())

    # Distribution des vues et likes (si les colonnes existent)
    if 'views' in df.columns:
        print("\nDistribution des vues :")
        print(df['views'].describe())
    
    if 'likes' in df.columns:
        print("\nDistribution des likes :")
        print(df['likes'].describe())

# Appel de la fonction d'exploration
explore_data()
