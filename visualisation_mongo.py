import pymongo
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import certifi

# Titre de l'application
st.title("📊 Tableau de bord YouTube - Analyse MongoDB")

# Connexion sécurisée à MongoDB Atlas avec certifi
try:
    client = pymongo.MongoClient(
        "mongodb+srv://eliiimk:29092231Emk@cluster0.qd63n.mongodb.net/?retryWrites=true&w=majority",
        tlsCAFile=certifi.where()
    )
    client.admin.command('ping')  # Vérifie la connexion à MongoDB
except Exception as e:
    st.error(f"❌ Erreur de connexion à MongoDB Atlas : {e}")
    st.stop()

# Accès à la base de données et à la collection
db = client['youtube_project']
collection = db['videos']

# Chargement des données avec cache Streamlit
@st.cache_data(ttl=600)
def load_data():
    data = list(collection.find({}, {"_id": 0}))
    return pd.DataFrame(data)

df = load_data()

# Si la base de données est vide
if df.empty:
    st.warning("⚠️ Aucune donnée trouvée dans la base de données.")
    st.stop()

# Traitement de la date
if 'publishedAt' in df.columns:
    df['publishedAt'] = pd.to_datetime(df['publishedAt'])

# Filtrage par chaîne
if 'channelTitle' in df.columns:
    st.sidebar.header("🎚️ Filtres")
    selected_channels = st.sidebar.multiselect(
        "Sélectionnez une ou plusieurs chaînes :",
        options=df['channelTitle'].unique(),
        default=df['channelTitle'].unique()
    )
    df = df[df['channelTitle'].isin(selected_channels)]

# Bouton pour réinitialiser les filtres
if st.sidebar.button("🔁 Réinitialiser les filtres"):
    st.experimental_rerun()

# Affichage des données
st.write("### 📋 Données des vidéos")
st.dataframe(df)

# Téléchargement CSV
csv = df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="📥 Télécharger les données au format CSV",
    data=csv,
    file_name='videos_youtube.csv',
    mime='text/csv',
)

# Graphique 1 : Nombre de vidéos par chaîne
if 'channelTitle' in df.columns:
    channel_counts = df['channelTitle'].value_counts()
    st.subheader("📌 Nombre de vidéos par chaîne")
    plt.figure(figsize=(10, 6))
    channel_counts.plot(kind='bar', color='skyblue', edgecolor='black')
    plt.xlabel('Chaîne')
    plt.ylabel('Nombre de vidéos')
    plt.title('Nombre de vidéos par chaîne')
    plt.tight_layout()
    st.pyplot(plt)

# Graphique 2 : Nombre de vidéos publiées par mois
if 'publishedAt' in df.columns:
    df['year_month'] = df['publishedAt'].dt.to_period('M')
    monthly_counts = df['year_month'].value_counts().sort_index()
    st.subheader("📅 Nombre de vidéos publiées par mois")
    plt.figure(figsize=(10, 6))
    monthly_counts.plot(kind='bar', color='lightgreen', edgecolor='black')
    plt.xlabel('Mois')
    plt.ylabel('Nombre de vidéos')
    plt.title('Nombre de vidéos publiées par mois')
    plt.tight_layout()
    st.pyplot(plt)

    # Nombre de vidéos publiées par semaine
    df['week'] = df['publishedAt'].dt.to_period('W').astype(str)
    weekly_counts = df['week'].value_counts().sort_index()
    st.subheader("📆 Nombre de vidéos publiées par semaine")
    plt.figure(figsize=(12, 6))
    weekly_counts.plot(kind='bar', color='orange', edgecolor='black')
    plt.xlabel('Semaine')
    plt.ylabel('Nombre de vidéos')
    plt.title("Nombre de vidéos par semaine")
    plt.tight_layout()
    st.pyplot(plt)

# Graphique 3 : Répartition en camembert
if 'channelTitle' in df.columns:
    st.subheader("📈 Répartition des vidéos par chaîne")
    channel_counts = df['channelTitle'].value_counts()
    plt.figure(figsize=(8, 8))
    channel_counts.plot(kind='pie', autopct='%1.1f%%', startangle=90,
                        colors=['#66b3ff', '#99ff99', '#ffcc99', '#ff9999', '#c2c2f0', '#ffb3e6'] * 10)
    plt.ylabel('')
    plt.title('Répartition des vidéos par chaîne')
    plt.tight_layout()
    st.pyplot(plt)
