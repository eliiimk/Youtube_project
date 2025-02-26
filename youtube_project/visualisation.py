import pymongo
import pandas as pd
import matplotlib.pyplot as plt

# Connexion à MongoDB
client = pymongo.MongoClient("mongodb+srv://eliimk:29092231Emk@cluster0.qd63n.mongodb.net/?retryWrites=true&w=majority")
db = client["youtube_project"]
collection = db["videos"]

# Récupération des données
data = list(collection.find({}, {"_id": 0}))  # Exclut le champ _id
df = pd.DataFrame(data)

# Exemple : afficher un graphique de la distribution des prix des vidéos
plt.figure(figsize=(10,6))
plt.hist(df['price'], bins=20, color='skyblue', edgecolor='black')
plt.title('Distribution des prix des vidéos')
plt.xlabel('Prix')
plt.ylabel('Nombre de vidéos')
plt.show()
