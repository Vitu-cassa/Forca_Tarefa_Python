ativos = [
    {"nome": "SRV-WEB01", "tipo": "servidor", "ip": "192.168.1.10", "status": "ativo"},
    {"nome": "PC-RH03",   "tipo": "estacao",  "ip": "192.168.1.45", "status": "ativo"},
    {"nome": "SW-CORE01", "tipo": "switch",   "ip": "192.168.1.1",  "status": "inativo"},
]

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
'''Exercício 2.1 — CRUD de inventário de ativos
        Crie um programa com menu que gerencie um inventário de ativos no MongoDB.
        Opções:
        [1] cadastrar,
        [2] listar,
        [3] buscar por IP,
        [4] atualizar status,
        [5] remover,
        [6] sair.
        
        Impeça IPs duplicados (dica: índice único create_index("ip", unique=True)).

        # Dados iniciais para popular a coleção:
        ativos = [
            {"nome": "SRV-WEB01", "tipo": "servidor", "ip": "192.168.1.10", "status": "ativo"},
            {"nome": "PC-RH03",   "tipo": "estacao",  "ip": "192.168.1.45", "status": "ativo"},
            {"nome": "SW-CORE01", "tipo": "switch",   "ip": "192.168.1.1",  "status": "inativo"},
        ]

        # Sequência de teste e saída esperada:
        # [1] Cadastrar SRV-DB01 / 192.168.1.20  -> "Ativo cadastrado!"
        # [1] Cadastrar com ip=192.168.1.10       -> "Erro: IP já cadastrado!"
        # [3] Buscar 192.168.1.45                 -> exibe dados do PC-RH03
        # [4] Atualizar 192.168.1.1 para "ativo"  -> "Status atualizado!"
        # [2] Listar                              -> tabela com os 4 ativos
'''
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
from pymongo import MongoClient
from datetime import datetime
from datetime import datetime, timedelta
import random
from time import sleep

def _apresentacao():
    '''
    Cabeçalho do exercicio.
    '''
    print("+------------------------+")
    print("| Gerenciador de ativos  |")
    print("+------------------------+")
    print()

def _menu():
    '''
    Apresenta as opções na tela para usuario escolher.
    '''
    print("Escolha uma das opçoes abaixo:")
    print(
        "[1] cadastrar\n"
        "[2] listar\n"
        "[3] buscar por IP\n"
        "[4] atualizar status\n"
        "[5] remover\n"
        "[6] Sair\n"
    )
    # print("[2] listar")
    # print("[3] buscar por IP")
    # print("[4] atualizar status")
    # print("[5] remover")
    # print("[6] Sair")

def _conexaoMongo():
    '''
    Realiza conexao com o banco para criar coleção.
    '''
    client = MongoClient("mongodb://localhost:27017/")
    # Testa coenxão
    client.admin.command("ping")
    print("\nConectado ao MongoDB!")
    sleep(0.5)

    print("Preparando banco...")
    db = client["seguranca"]
    sleep(1)

    print("Criando coleção...\n")
    ativos = db["ativos"]

def _main():

    '''
    Função principal.
    '''

    _conexaoMongo()
    escolha = 0

    while True:
        sleep(2)

        _apresentacao()
        _menu()

        escolha = input("Digite a opção desejada: ")

        if escolha == "1":
            sleep(2)
            print("Opção {} em construção!".format(escolha))
        elif escolha == "2":
            sleep(2)
            print("Opção {} em construção!".format(escolha))
        elif escolha == "3":
            sleep(2)
            print("Opção {} em construção!".format(escolha))
        elif escolha == "4":
            sleep(2)
            print("Opção {} em construção!".format(escolha))
        elif escolha == "5":
            sleep(2)
            print("Opção {} em construção!".format(escolha))
        elif escolha == "6":
            print("Opção {}\n"
            "saindo da aplicação...".format(escolha))
            sleep(2)
            break
        else:
            sleep(2)
            print("Opção inválida, faça uma sugestão ao dev!")

_main()