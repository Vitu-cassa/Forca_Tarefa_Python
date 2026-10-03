from pymongo import MongoClient


client = MongoClient("mongodb://localhost:27017/")
db = client["seguranca"]            # banco
eventos = db["eventos"]             # coleção
alertas = db["alertas"]

# Boa prática: confirmar a conexão
client.admin.command("ping")
print("Conectado ao MongoDB!")
