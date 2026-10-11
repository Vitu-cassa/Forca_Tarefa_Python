lista_ativos = [
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
from time import sleep
from pymongo import errors

def _apresentacao():
    '''
    Cabeçalho do exercicio.
    '''
    
    print()
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

def _criadorInicial(lista, ativos):
    try:
        ativos.insert_many(lista)
    except Exception as e:
        print("Falha na inserção: {}".format(e))

def _deletadorTotal(db):
    try:
        # Busca a lista com o nome de todas as coleções ativas no banco
        for nome_colecao in db.list_collection_names():
            # Exclui a coleção inteira
            db[nome_colecao].drop()
            print(f"Coleção '{nome_colecao}' removida com sucesso.")

    except Exception as e:
        print(f"Erro ao limpar o banco: {e}")

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
        ativos = db["ativos"]
    except Exception as e:
        print("Falha na conexão com o banco: {}".format(e))
    finally:
        print("Indexando...")
        sleep(2)
        ativos.create_index("ip", unique = True)
    return ativos, db

def _listadorDeAtivos(colecao):
    '''
    Realiza a consulta de todos os ativos.
    '''
    try:
        for ativo in colecao.find({"ip": {"$exists": True}}):
            print("Nome: {:<15} | IP: {:<17} | Status: {}".format(ativo.get("nome"), ativo.get("ip"), ativo.get("status")))
    except Exception as e:
        print("Falha na consulta multipla: {}".format(e))

def _cadastradorDeAtivos(colecao):
    '''
    Realiza o cadastro de um novo ativo ao banco.
    '''
    ativo = {}
    try:
        ativo["nome"] = str(input("Nome: "))
        ativo["tipo"] = str(input("Tipo: "))
        ativo["ip"]= str(input("ip: "))
        ativo["status"]= str(input("Status: "))

        res = colecao.insert_one(ativo)
        print(res.inserted_id)

    except errors.DuplicateKeyError:
        print("Ativo ja cadastrado!")
    except Exception as e:
        print("Falha na atualização da coleção: {}".format(e))

def _pesquisadorDeAtivos(colecao, ip):
    try:
        ativo = colecao.find_one({"ip": ip})
        if ativo:
            print("\n"
                "Ativo encontrado:\n"
                "Nome: {:<15} | Tipo: {:<17} | Status: {}"
                .format(ativo.get("nome"), ativo.get("tipo"), ativo.get("status"))
            )
            return True
        else:
            print("\nIP não cadastrado!")
            return False
    except Exception as e:
        print("Falha na consulta unitária: {}".format(e))

def _atualizadorDeAtivos(colecao):
    '''
    Função atualiza um ativo do banco.
    '''
    ip = input("Indique o IP do ativo para atualiza: ")
    ativo_existe = _pesquisadorDeAtivos(colecao, ip)

    if ativo_existe:

        print("Indique os novos campos do ativo: ")
        novo_nome = str(input("Nome: "))
        novo_tipo = str(input("Tipo: "))
        novo_ip = str(input("ip: "))
        novo_status = str(input("Status: "))
        try:
            colecao.update_one(
                        {"ip": ip},
                        {"$set":
                            {
                            "nome": novo_nome,
                            "tipo": novo_tipo,
                            "ip": novo_ip,
                            "status": novo_status
                            }
                        }
                    )
            print("ativo atualizado!")

        except Exception as e:
            print("Falha na atualização: {}".format(e))

def _removedorDeAtivos(colecao):
    ip = input("Indique o IP do ativo para remover: ")
    ativo_existe = _pesquisadorDeAtivos(colecao, ip)

    if ativo_existe:

        print("Removendo ativo...")
        sleep(2)

        try:
            colecao.delete_one(
                        {"ip": ip}
                    )
            print("ativo deletado!")

        except Exception as e:
            print("Falha na atualização: {}".format(e))
def _main():
    '''
    Função principal.
    '''
    ativos, banco = _conexaoMongo()
    _criadorInicial(lista_ativos, ativos)

    escolha_menu = 0

    while True:
        sleep(2)

        _apresentacao()
        _menu()

        escolha_menu = input("Digite a opção desejada: ")

        if escolha_menu == "1":
            print("Indique os dados do ativo:")
            sleep(2)
            _cadastradorDeAtivos(ativos)

        elif escolha_menu == "2":
            print("Consultando ativos cadastrados...")
            sleep(2)
            print("Opção {} em construção!".format(escolha_menu))
            _listadorDeAtivos(ativos)

        elif escolha_menu == "3":
            ip = input("Indique o IP do ativo: ")
            print("Buscando ativo...")
            sleep(2)
            _pesquisadorDeAtivos(ativos, ip)

        elif escolha_menu == "4":
            sleep(2)
            _atualizadorDeAtivos(ativos)

        elif escolha_menu == "5":
            sleep(2)
            _removedorDeAtivos(ativos)

        elif escolha_menu == "6":
            print(
                "Opção {}\n"
                "deseja deletar o banco? [S]im / [N]ão".format(escolha_menu))
            apagar = input("Digite sua escolha: ")
            if apagar == "S":
                sleep(2)
                print("Deletando banco...")
                _deletadorTotal(banco)
            else:
                print("Dados mantidos para novos testes.")
            break

        else:
            sleep(2)
            print("Opção inválida, faça uma sugestão ao dev!")

_main()

# !!!!!!!!!! Aera dev !!!!!!!!!!

# ativos, banco = _conexaoMongo()
# _criadorInicial(lista_ativos, ativos)

# _listadorDeAtivos(ativos)