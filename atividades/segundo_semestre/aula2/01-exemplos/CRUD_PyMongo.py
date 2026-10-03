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

# CREATE — inserir um ou muitos
evento = {
    "timestamp": datetime(2025, 2, 20, 8, 15, 1),
    "fonte": "auth", "tipo": "FAIL",
    "ip": "185.220.101.1", "detalhes": {"usuario": "admin"}
}
res = eventos.insert_one(evento)
print(res.inserted_id)                       # ObjectId gerado

evento1 = {
    "timestamp": datetime(2025, 2, 20, 8, 15, 1),
    "fonte": "auth", "tipo": "FAIL",
    "ip": "185.220.101.2", "detalhes": {"usuario": "admin2"}
}
evento2 = {
    "timestamp": datetime(2025, 2, 20, 8, 15, 1),
    "fonte": "auth", "tipo": "FAIL",
    "ip": "185.220.101.3", "detalhes": {"usuario": "admin3"}
}
evento3 = {
    "timestamp": datetime(2025, 2, 20, 8, 15, 1),
    "fonte": "auth", "tipo": "FAIL",
    "ip": "185.220.101.4", "detalhes": {"usuario": "admin4"}
}
eventos.insert_many([evento1, evento2, evento3])

# READ — find_one e find (com filtro, projeção, ordenação)
um = eventos.find_one({"ip": "185.220.101.1"})
for doc in eventos.find({"tipo": "FAIL"}, {"_id": 0, "ip": 1, "timestamp": 1}).sort("timestamp", -1):
    print(doc)

# Operadores de consulta
eventos.find({"detalhes.tentativas": {"$gt": 5}})            # maior que
eventos.find({"tipo": {"$in": ["FAIL", "BLOCK"]}})           # em uma lista
eventos.find({"ip": {"$regex": "^185\\."}})                  # regex

# UPDATE
alertas.update_one({"cve_id": "CVE-2024-001"}, {"$set": {"corrigida": True}})
alertas.update_many({"severidade": "baixa"}, {"$set": {"revisado": True}})

# DELETE
alertas.delete_one({"cve_id": "CVE-2024-001"})
alertas.delete_many({"status": "resolvido"})

# COUNT
print(eventos.count_documents({"tipo": "FAIL"}))