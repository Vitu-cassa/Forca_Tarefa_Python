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