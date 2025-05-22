from pymongo import MongoClient
import certifi

uri = "mongodb+srv://eliiimk:29092231Emk@cluster0.qd63n.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri, tlsCAFile=certifi.where())

try:
    print("Connexion réussie ✅")
    print(client.list_database_names())
except Exception as e:
    print("Échec de connexion ❌")
    print(e)
