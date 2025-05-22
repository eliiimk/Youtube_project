from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from youtube_project import YouTubeDataPipeline, clean_data, explore_data


# Charge les variables d'environnement
from dotenv import load_dotenv
load_dotenv()

# Récupère les variables d'environnement
API_KEY = os.getenv("API_KEY")
CHANNEL_NAME = os.getenv("CHANNEL_ID")
MONGO_URI = os.getenv("MONGO_URI")

# Crée le pipeline YouTube
pipeline = YouTubeDataPipeline(MONGO_URI, "youtube_project", API_KEY)

# Définition du DAG
default_args = {
    'owner': 'eli',
    'start_date': datetime(2024, 3, 10),
    'catchup': False
}

with DAG(
    'youtube_pipeline',
    default_args=default_args,
    schedule_interval='@daily',  # Exécute tous les jours
    catchup=False
) as dag:

    def fetch_and_store():
        pipeline.fetch_and_store_data(CHANNEL_NAME)

    def clean():
        clean_data()

    def explore():
        explore_data()

    # Tâches Airflow
    task_fetch_and_store = PythonOperator(
        task_id='fetch_and_store',
        python_callable=fetch_and_store
    )

    task_clean_data = PythonOperator(
        task_id='clean_data',
        python_callable=clean
    )

    task_explore_data = PythonOperator(
        task_id='explore_data',
        python_callable=explore
    )

    # Définition de l'ordre d'exécution des tâches
    task_fetch_and_store >> task_clean_data >> task_explore_data
