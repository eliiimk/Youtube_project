import streamlit as st
import pymongo
import pandas as pd

# Connexion à MongoDB
client = pymongo.MongoClient("mongodb+srv://eliiimk:29092231Emk@cluster0.qd63n.mongodb.net/?retryWrites=true&w=majority")
db = client['nom_de_votre_base']
collection = db['nom_de_votre_collection']

# Récupération des données
data = list(collection.find({}, {"_id": 0}))  # Exclut le champ _id
df = pd.DataFrame(data)

# Affichage des données sous forme de tableau dans Streamlit
st.write(df)

# Exemple de graphique interactif avec les données (exemple avec la colonne 'price')
st.bar_chart(df['price'])
