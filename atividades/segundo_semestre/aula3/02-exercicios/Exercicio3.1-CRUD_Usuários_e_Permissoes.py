usuarios = [
    ("Carlos Silva", "carlos@empresa.com", 3),
    ("Ana Costa",    "ana@empresa.com",    5),
    ("Bruno Lima",   "bruno@empresa.com",  1),
]

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
'''Exercício 3.1 — CRUD de usuários e permissões
        Crie um sistema com menu que gerencie usuários no MySQL
        (tabela usuarios com id, nome, email único, nivel_acesso 1–5).
        Opções: cadastrar, listar, buscar por email, promover/rebaixar nível,
        remover. Todas as queries devem ser parametrizadas.
        Valide nível entre 1 e 5.

        # Dados iniciais:
        usuarios = [
            ("Carlos Silva", "carlos@empresa.com", 3),
            ("Ana Costa",    "ana@empresa.com",    5),
            ("Bruno Lima",   "bruno@empresa.com",  1),
        ]

        # Sequência de teste:
        # Cadastrar email duplicado (carlos@empresa.com) -> "Erro: email já existe"
        # Buscar ana@empresa.com                          -> exibe nível 5
        # Promover Bruno para nível 4                      -> "Nível atualizado!"

        # Saída esperada (listar após operações):
        # Carlos Silva | carlos@empresa.com | nível 3
        # Ana Costa    | ana@empresa.com    | nível 5
        # Bruno Lima   | bruno@empresa.com  | nível 4
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

def _criadoeDeTabela(conexao, cursor):
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

def _listadorDeUsuarios(conexao, cursor):
    '''
    Função consulta e retorna todos os dados dos usuários castrados.
    '''
    cursor = conexao.cursor(dictionary=True)
    try:
        cursor.execute(
            "SELECT * FROM usuarios"
        )
        for linha in cursor.fetchall():
            print(
                "{:<15} | email: {:<20} | Nível {}".format(linha["nome"],
                                                           linha["email"],
                                                           linha["nivel_acesso"])
            )
        conexao.commit()
    except Exception as e:
        print("Falha na consulta: {}".format(e))

def _cadastradorDeUsuarios(conexao, cursor, usuario):
    '''
    Função recebe os dados de novo usuário e o insere no banco.
    '''
    try:
        cursor.execute(
            "INSERT INTO usuarios(nome, email, nivel_acesso)" \
            "VALUES(%s,%s,%s)", usuario
        )
        conexao.commit()
        print("Cadastro realizado!")
    except Exception as e:
        print("Cadastro não realizado: {}".format(e))

def _buscadorDeUsuarios(conexao, cursor, busca):
    '''
    Função busca um usuário pelo campo de emial.
    '''
    cursor = conexao.cursor(dictionary=True)
    try:
        cursor.execute(
            "SELECT nome, nivel_acesso FROM usuarios " \
            "WHERE email = %s", (busca, )
        )
        for linha in cursor.fetchall():
            print(
                "Usuário localizaso\n" \
                "{} -> nivel {}".format(linha["nome"],
                                        linha["nivel_acesso"]))
    except Exception as e:
        print("Busca não realizada: {}".format(e))

def _atualizadorDeCampos(conexao, cursor, atualiza_nivel):
    '''
    Funão Realiza a mudança do nivel de acesso de um usuario.
    '''
    try:
        cursor.execute(
            "UPDATE usuarios SET nivel_acesso = %s " \
            "WHERE email = %s", atualiza_nivel
        )
        conexao.commit()
        print("Nivel atualizado!")
    except Exception as e:
        print("Atualização falhou: {}".format(e))

def _removedorDeusUario(conexao, cursor, email_remover):
    '''
    Deleta um usuario do banco
    '''
    try:
        cursor.execute(
            "DELETE FROM usuarios WHERE email = %s", (email_remover, )
        )
        conexao.commit()
        print("Usuario removido!")
    except Exception as e:
        print("Remoção fracassou: {}".format(e))

def _main():
    '''
    Função principal.
    '''
    conexao, cursor = _conectorSql()
    _criadoeDeTabela(conexao, cursor)
    _preenchedorInicial(conexao, cursor, usuarios)
    escolha_menu = 0

    while True:
        sleep(2)

        _apresentacao()
        _menu()
        escolha_menu = input("Digite a opção desejada: ")

        if escolha_menu == "1":
            novo_usuario = []
            print("Indique os dados do Usuário:")
            for campo in ("nome completo", "email", "nivel_acesso"): 
                novo_usuario.append(input("{}: ".format(campo)))
            sleep(2)
            _cadastradorDeUsuarios(conexao, cursor, novo_usuario)

        elif escolha_menu == "2":
            print("Listando usários cadastrados...")
            sleep(2)
            _listadorDeUsuarios(conexao, cursor)

        elif escolha_menu == "3":
            busca = input("Indique o email do usuário: ")
            print("Buscando usuário...")
            sleep(2)
            _buscadorDeUsuarios(conexao, cursor, busca)

        elif escolha_menu == "4":
            atualiza_nivel = []
            print("Indique o novo nível de acesso e o email do usuário:")
            for campo in ("novo nivel", "email"): 
                atualiza_nivel.append(str(input("{}: ".format(campo))))
            sleep(2)
            _atualizadorDeCampos(conexao, cursor, atualiza_nivel)

        elif escolha_menu == "5":
            email_remover = input("Indique o email a ser removido: ")
            sleep(2)
            _removedorDeusUario(conexao, cursor, email_remover)

        elif escolha_menu == "6":
            print(
                "Opção {}\n"
                "deseja deletar a tabela? [S]im / [N]ão".format(escolha_menu))
            apagar = input("Digite sua escolha: ")
            if apagar == "S":
                print("Deletando tabela...")
                sleep(2)
                _deletadorDeTabela(conexao, cursor)

            else:
                print("Dados mantidos para novos testes.")
            break

        else:
            sleep(2)
            print("Opção inválida, faça uma sugestão ao dev!")

_main()
