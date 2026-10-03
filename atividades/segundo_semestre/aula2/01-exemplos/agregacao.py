from datetime import datetime
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["seguranca"]            # banco
eventos = db["eventos"]             # coleção
alertas = db["alertas"]

# Boa prática: confirmar a conexão
client.admin.command("ping")
print("Conectado ao MongoDB!")

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
pipeline = [
    {"$match": {"tipo": "FAIL"}},                                  # filtra
    {"$group": {"_id": "$ip", "total": {"$sum": 1}}},              # agrupa e conta
    {"$sort": {"total": -1}},                                      # ordena
    {"$limit": 10}                                                 # top 10
]
for linha in eventos.aggregate(pipeline):
    print(f"{linha['_id']}: {linha['total']} falhas")
    