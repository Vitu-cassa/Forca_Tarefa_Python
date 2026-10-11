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