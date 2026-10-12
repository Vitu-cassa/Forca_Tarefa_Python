usuarios = [
    ("Carlos Silva", "carlos@empresa.com", 3),
    ("Ana Costa",    "ana@empresa.com",    5),
    ("Bruno Lima",   "bruno@empresa.com",  1),
]

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
'''Exercício 3.2 — Prova de conceito de SQL Injection (defensivo)
        Escreva duas funções de busca de usuário por nome: buscar_inseguro(nome)
        (concatenando) e buscar_seguro(nome) (parametrizado). Demonstre com a entrada
        maliciosa ' OR '1'='1 que a primeira retorna todos os usuários e a segunda
        retorna nenhum. Documente o resultado.

        entrada_maliciosa = "' OR '1'='1"

        # Saída esperada:
        # [INSEGURO] entrada: ' OR '1'='1  -> 3 usuários retornados (VAZAMENTO!)
        # [SEGURO]   entrada: ' OR '1'='1  -> 0 usuários retornados (defesa OK)
        # Conclusão: a query parametrizada tratou a entrada como texto literal.
'''
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

import mysql.connector
from time import sleep
from datetime import datetime

def _apresentacao():
    '''
    Cabeçalho do exercicio.
    '''

    print()
    print("+----------------------------------------+")
    print("|  Gerenciador de Usuários e permissões  |")
    print("+----------------------------------------+")
    print()

def _menu():
    '''
    Apresenta as opções na tela para usuario escolher.
    '''
    print("Escolha uma das opçoes abaixo:")
    print(
        "[1] cadastrar\n"
        "[2] listar\n"
        "[3] buscar por e-mail\n"
        "[4] Promover/Rebaixar nível\n"
        "[5] remover\n"
        "[6] Sair\n"
    )

def _conectorSql():
    '''
    Conecta ao MySQL
    '''
    try:
        conexao = mysql.connector.connect(
            host="localhost", user="root",
            password="senha", database="seguranca"
        )
        if conexao.is_connected():
            print("Conectado ao MySQL!")
    except Exception as e:
        print(f"Erro de conexão: {e}")

    finally:
        cursor = conexao.cursor()
    return conexao, cursor

def _criadorDeTabela(conexao, cursor):
    '''
    Cria a tabela de usuários.
    '''
    try:
        print("tomara que esteja criando a tabela...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios(
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    nome VARCHAR(50),
                    email VARCHAR(45) UNIQUE,
                    nivel_acesso ENUM('1', '2', '3', '4', '5'),
                    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
        """)
    except Exception as e:
        print("Tabela não criada: {}".format(e))

def _preenchedorInicial(conexao, cursor, lista):
    '''
    Função preenche do dados iniciais na tabela criada.
    '''
    try:
        cursor.executemany(
            "INSERT INTO usuarios (nome, email, nivel_acesso) " \
            "VALUES(%s,%s,%s)", lista
        )
        conexao.commit()
    except Exception as e:
        print("Erro no preenchimento inicial: {}".format(e))

def _buscadorDeUsuariosParametrizado(conexao, cursor, busca):
    '''
    Função busca um usuário pelo campo de emial.
    '''
    cursor = conexao.cursor(dictionary=True)
    try:
        cursor.execute(
            "SELECT * FROM usuarios " \
            "WHERE email = %s", (busca, )
        )
        for linha in cursor.fetchall():
            print(
                "Usuário localizado\n" \
                "{} -> nivel {}".format(linha["nome"],
                                        linha["nivel_acesso"]))
    except Exception as e:
        print("Busca não realizada: {}".format(e))

def _buscadorDeUsuariosInjection(conexao, cursor, busca):
    '''
    Função busca um usuário pelo campo de emial.
    '''
    cursor = conexao.cursor(dictionary=True)
    try:
        cursor.execute(
            "SELECT * FROM usuarios " \
            "WHERE email = '{}'".format(busca)
        )
        for linha in cursor.fetchall():
            print(
                "Usuário localizado\n" \
                "{} -> nivel {}".format(linha["nome"],
                                        linha["nivel_acesso"]))
        conexao.commit()
    except Exception as e:
        print("Busca não realizada: {}".format(e))


def _deletadorDeTabela(conexao, cursor):
    '''
    Remove todas as tabelas do banco.
    '''
    try:
        cursor.execute(
            "DROP TABLE IF EXISTS usuarios"
        )
        conexao.commit()
        print("Tabela apagada!")
    except Exception as e:
        print("Remoção falhou: {}".format(e))

def _main():
    '''
    Função principal.
    '''
    print(
        52*"!", \
        "\n Nao utilizar a entrada ' OR '1'='1 como parametro \n", \
        52*"!"
    )
    conexao, cursor = _conectorSql()
    _criadorDeTabela(conexao, cursor)
    _preenchedorInicial(conexao, cursor, usuarios)
    email = input("Indique o email para teste: ")
    print("\nTestando com busca parametrizada...")
    sleep(2)
    _buscadorDeUsuariosParametrizado(conexao, cursor, email)
    print("\nTestando com busca não parametrizada...")
    sleep(2)
    _buscadorDeUsuariosInjection(conexao, cursor, email)
    _deletadorDeTabela(conexao, cursor)
    sleep(2)
    if 'conexao' in locals() and conexao.is_connected():
        conexao.close()
    

_main()

