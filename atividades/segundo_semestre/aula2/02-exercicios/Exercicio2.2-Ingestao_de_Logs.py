# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
'''Exercício 2.2 — Ingestão de logs do 1º semestre no MongoDB
        Reaproveite o auth.log da GS do 1º semestre. Escreva um script que leia
        o arquivo, normalize cada linha em um documento e insira todos com
        insert_many. Depois, use um pipeline de agregação para
        listar os IPs com mais falhas.

        # Formato de cada linha do auth.log:
        # 2025-02-20 08:15:01 FAIL usuario=admin ip=185.220.101.1

        # Dica: parseie com split(), monte o dict, acumule numa lista
        #       e use insert_many.
        # Pipeline: $match tipo=FAIL -> $group por ip -> $sort desc -> $limit 5

        # Saída esperada (com o auth.log da GS, 23 linhas):
        # === Top IPs por falhas de login ===
        # 185.220.101.1 -> 10 falhas
        # 91.240.118.172 -> 5 falhas
        # 45.33.32.156  -> 3 falhas
        # Total de eventos inseridos: 23
'''
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
from pymongo import MongoClient
from pathlib import Path
from datetime import datetime
from time import sleep

diretorio_atual = Path(__file__).parent
auth_log = diretorio_atual.parent /"99-miscelanea"/"auth.log"

def _conexaoMongo():
    '''
    Realiza conexao com o banco para criar coleção.
    '''
    try:
        client = MongoClient("mongodb://localhost:27017/")
        # Testa conexão
        client.admin.command("ping")
        print("\nConectado ao MongoDB!")
        sleep(0.5)

        print("Preparando banco...")
        db = client["seguranca"]
        sleep(1)

        print("Criando coleção...\n")
        logs = db["logs"]
    except Exception as e:
        print("Falha na conexão com o banco: {}".format(e))
    finally:
        print("Indexando...")
        sleep(2)
        logs.create_index("ip")

    return logs, db

def _normalizadorDeLogs(pedaco):
    '''
    Lê a linha do log, retorna um dicionario para popular a coleção do banco.
    '''
    timestamp = (pedaco[0] + " " + pedaco[1])
    tipo = pedaco[2]

    for parte in pedaco[3:]:

        if parte.startswith("usuario="):
            usuario = parte[8:]

        elif parte.startswith("ip="):
            ip = parte[3:]

    resultado = {
        "timestamp": timestamp,
        "tipo": tipo,
        "usuario": usuario,
        "ip": ip
    }


    return resultado

def _criadorInicial(lista, colecao):
    try:
        colecao.insert_many(lista)
    except Exception as e:
        print("Falha na inserção: {}".format(e))

def _pipelinezador(colecao):
    '''
    Realiza o pipeline e imprime a saida do ranking
    '''
    pipeline = [
        {"$match": {"tipo": "FAIL"}},
        {"$group": {"_id": "$ip", "total": {"$sum": 1}}},
        {"$sort": {"total": -1}},
        {"$limit": 5}
    ]

    for linha in colecao.aggregate(pipeline):
        sleep(0.5)
        print("{:<15} -> {} Falhas".format(linha["_id"], linha["total"]))

def _main():
    '''
    Função principal
    '''
    log_normalizado = []

    if auth_log.exists():
        try:
            with open(auth_log, "r", encoding="UTF-8") as arquivo:
                for linha in arquivo:
                    pedaco = linha.strip().split(" ")

                    log_normalizado.append((_normalizadorDeLogs(pedaco)))
        except Exception as e:
            print("Falha na normalização do auth.log: {}".format(e))

    logs, bd = _conexaoMongo()
    _criadorInicial(log_normalizado, logs)

    print("\n=== Top IPs por falhas de login ===")
    sleep(1)
    _pipelinezador(logs)

_main()

