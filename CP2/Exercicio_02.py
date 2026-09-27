
ativos  = [(1,"SRV-WEB01","192.168.1.10","alta"), (2,"PC-RH03","192.168.1.45","baixa")]
alertas = [(1,1,"BRUTE_FORCE","critica"), (2,1,"PORT_SCAN","alta"), (3,2,"XSS","media")]

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
''' Exercício 2 — Migração relacional → documentos (Aulas 1, 2 e 3):
        O cadastro está normalizado em MySQL (ativos 1—N alertas). Migre para o
        MongoDB no modelo de documentos, aninhando os dados do ativo dentro de
        cada alerta, e prove que nada se perdeu no caminho.

        # MySQL (crie e popule):
        # ativos(id PK, nome, ip UNIQUE, criticidade ENUM('baixa','media','alta'))
        # alertas(id PK, ativo_id FK, tipo, severidade, criado_em)

        ativos  = [(1,"SRV-WEB01","192.168.1.10","alta"), (2,"PC-RH03","192.168.1.45","baixa")]
        alertas = [(1,1,"BRUTE_FORCE","critica"), (2,1,"PORT_SCAN","alta"), (3,2,"XSS","media")]

        # 1. Leia com um JOIN parametrizado.
        # 2. Monte documentos assim e insira com insert_many:
        # {"tipo":"BRUTE_FORCE","severidade":"critica",
        #  "ativo":{"nome":"SRV-WEB01","ip":"192.168.1.10","criticidade":"alta"}}
        # 3. Verifique a migração: conte no MySQL e no Mongo e compare.

        # Saída esperada:
        # MySQL: 3 alertas | MongoDB: 3 documentos -> MIGRAÇÃO ÍNTEGRA
        # Consulta sem JOIN: db.alertas.find({"ativo.criticidade":"alta"}) -> 2 documentos
        # Comentário (2 linhas): o que se ganha (leitura sem JOIN) e o que se perde
        #                        (duplicação: renomear o ativo exige update_many).
'''
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# importa módulos para o programa

import mysql.connector
from mysql.connector import Error
from pymongo import MongoClient
from pymongo.errors import PyMongoError # Tentei usar isso mas não gostei
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
import time

def _criaTabelaSQL():
    '''
    cria as tabelas para exercicio
        MySQL (crie):
        ativos(id PK, nome, ip UNIQUE, criticidade ENUM('baixa','media','alta'))
    '''
    # Cria tabela
    try:
        print("Demolindo tabelas antigas...")

        cursor.execute("DROP TABLE IF EXISTS alertas")
        cursor.execute("DROP TABLE IF EXISTS ativos")
        conexao.commit()
        time.sleep(3)
        print("Criando Tabelas novas")
        cursor.execute("""
            CREATE TABLE ativos(
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        nome VARCHAR(20),
                        ip VARCHAR(25) UNIQUE,
                        criticidade ENUM('baixa', 'media', 'alta'),
                        criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                        )
        """)

        cursor.execute("""
            CREATE TABLE alertas(
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    ativo_id INT,
                    FOREIGN KEY (ativo_id) REFERENCES ativos(id),
                    tipo VARCHAR(20),
                    severidade VARCHAR(20),
                    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
        """)

    except Error as e:
        print("Tabela não criada: {}".format(e))

def _inserirDadosMysql():

    print("Preenchendo tabelas MySQL...")
    try:
        cursor.executemany(
            "INSERT INTO ativos (id, nome, ip, criticidade) \
            VALUES (%s, %s, %s, %s)", ativos
         )
        conexao.commit()
        
        cursor.executemany(
            "INSERT INTO alertas (id, ativo_id, tipo, severidade) \
            VALUES (%s, %s, %s, %s)", alertas
         )
        conexao.commit()
    except Error as e:
        print("Dados não cadastrado: {}".format(e))

def _realizadorJoin():
    cursor = conexao.cursor(dictionary=True)
    dados_mongo = []
    contador_sql = 0

    try:
        cursor.execute("""
            SELECT 
                ativos.id AS ativo_id,
                ativos.nome,
                ativos.ip,
                ativos.criticidade,
                ativos.criado_em AS ativo_criado_em,
                
                alertas.id AS alerta_id,
                alertas.tipo,
                alertas.severidade,
                alertas.criado_em AS alerta_criado_em
                
            FROM ativos
            JOIN alertas 
                ON ativos.id = alertas.ativo_id;
        """)
        for linha in cursor.fetchall():
            dados_mongo.append(linha)
            contador_sql += 1
        
        return dados_mongo, contador_sql
    except Exception as e:
        print("JOIN não executado: {}".format(e))

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

try:
    conexao = mysql.connector.connect(
        host="localhost", user="root",
        password="senha", database="seguranca"
    )
    if conexao.is_connected():
        print("Conectado ao MySQL!")
except Error as e:
    print(f"Erro de conexão: {e}")

finally:
    cursor = conexao.cursor()

    _criaTabelaSQL()
    _inserirDadosMysql()
    dados_mongo, contador_sql = _realizadorJoin()

    if 'conexao' in locals() and conexao.is_connected():
        conexao.close()

# MONGO
apagar = input("Quer remover coleções anteriores? [S]im/[N]ão ")

# configurando conexão
client = MongoClient("mongodb://localhost:27017/")
db = client["seguranca"]
logs_db = db["logs"]

print(client.admin.command("ping"))
print("Conectado ao Mongo!")

if apagar == "S":
    # Limpando coleções antigas no banco
    print("Limpando todas as coleções antigas...")
    try:
        # Busca a lista com o nome de todas as coleções ativas no banco
        for nome_colecao in db.list_collection_names():
            # Exclui a coleção inteira
            db[nome_colecao].drop()
            print(f"Coleção '{nome_colecao}' removida com sucesso.")
            
        print("Banco de dados resetado com sucesso!")

    except Exception as e:
        print(f"Erro ao limpar o banco: {e}")

# Adicionando logs à coleção
print("Inserindo novos eventos...")
try:
    logs_db.insert_many(dados_mongo)
    print("{} novos logs catalogados.".format(logs_db.count_documents({})))
except Exception as e:
    print("Falha na inserção: {}".format(e))

# indexação para contagem
print("Indexando...")
try:
    logs_db.create_index("alertas")
except Exception as e:
    print("Indexação falhou: {}".format(e))

# Realiza contagem de alertas catalogados
try:
    contador_mongo = 0
    pipeline = [
        {"$group": {"_id": "$alertas", "total":{"$sum": 1}}},
        ]
    for log in logs_db.aggregate(pipeline):
        contador_mongo = log["total"]
except Exception as e:
    print("Falha na contagem de eventos: {}".format(e))

print("MySQL: {:<5} | Mongo: {:<5}".format(contador_sql, contador_mongo))