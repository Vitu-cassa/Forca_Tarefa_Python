
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
''' Exercício 3 — Retenção e janela temporal (Aula 2):
        Um SOC não guarda log para sempre nem olha o total — olha a janela.
        Crie a coleção eventos com um índice TTL, popule 200 eventos espalhados
        em 24 horas e produza, por agregação, a distribuição de falhas por hora
        do dia.

        # Dicas:
        # TTL:      eventos.create_index("timestamp", expireAfterSeconds=604800)   # 7 dias
        # Hora:     {"$group": {"_id": {"$hour": "$timestamp"}, "total": {"$sum": 1}}}
        # Filtro de janela: {"timestamp": {"$gte": datetime.now() - timedelta(hours=6)}}

        # Saída esperada (exemplo — seus números variam com a geração):
        # === Falhas por hora (últimas 24h) ===
        # 02h | ████████████ 34
        # 03h | ██████████████████ 51   <- pico
        # 09h | ███ 8
        # Hora de pico: 03h (51 falhas)
        # Índice TTL ativo: eventos com mais de 7 dias serão removidos automaticamente.
        # Comentário (1 linha): por que o TTL é uma decisão de segurança, não só de disco.
        ⚠️ O MongoDB roda a limpeza do TTL a cada ~60s; não espere exclusão instantânea no teste.
'''
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
from pymongo import MongoClient
from datetime import datetime
from datetime import datetime, timedelta
import random
from time import sleep

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# Criando carga para coleção de eventos.
# Gerado por vibe coding, a partir de um loop simples enviado para a IA.
# Logica dos prompts em "miscelanea/duvidas.md".
# Função auxiliar para verificar se um número é primo

def eh_primo(n):
    if n < 2:
        return False
    for j in range(2, int(n ** 0.5) + 1):
        if n % j == 0:
            return False
    return True

# Nova função que encapsula todo o processo de geração de eventos
def geraEventos(quantidade=200):
    '''
    funçao gera uma quantidade de eventos semi-aleatorios para aplicar na coleçã,
    os valores de alguns indices variam de acordo com a validação de "i".
    data e hora também são aleatorios. (Ao menos espero que sejam)
    '''
    ips = ["185.220.101.1", "91.240.118.172", "45.33.32.156", "192.168.1.10"]
    eventos_gerados = []
    data_base = datetime.now()

    for i in range(quantidade):
        # Lógica da data aleatória
        minutos_aleatorios = random.randint(1, 10000)
        segundos_aleatorios = random.randint(0, 59)
        data_evento = data_base - timedelta(minutes=minutos_aleatorios, seconds=segundos_aleatorios)

        # Determina o Tipo (Verifica primo primeiro)
        if eh_primo(i):
            tipo_evento = "SUSPEITO"
        else:
            tipo_evento = "ACESSO" if i % 2 == 0 else "CONSULTA"

        # Monta o dicionário do evento
        evento = {
            "id_evento": i + 1,
            "ip": ips[i % 4],
            "tipo": tipo_evento,
            "status": "OK" if i % 2 == 0 else "NOK",
            "atualizado_em": data_evento
        }
        eventos_gerados.append(evento)
        
    return eventos_gerados
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

eventos = geraEventos()
print(eventos)
# Conecta com o MongDB
apagar = input("Quer remover coleções anteriores? [S]im/[N]ão ")

# configurando conexão
client = MongoClient("mongodb://localhost:27017/")
db = client["seguranca"]
eventos_db = db["eventos"]

print(client.admin.command("ping"))
print("Conectado ao Mongo!")
sleep(2)

if apagar == "S":
    # Limpando coleções antigas no banco
    print("Limpando todas as coleções antigas...")
    sleep(2)

    try:
        # Busca a lista com o nome de todas as coleções ativas no banco
        for nome_colecao in db.list_collection_names():
            # Exclui a coleção inteira
            db[nome_colecao].drop()
            print(f"Coleção '{nome_colecao}' removida com sucesso.")
            
        print("Banco de dados resetado com sucesso!")

    except Exception as e:
        print(f"Erro ao limpar o banco: {e}")

# Adicionando eventos à coleção
print(f"\nInserindo novos eventos...")
try:
    eventos_db.insert_many(eventos)
    print("{} novos logs catalogados.".format(eventos_db.count_documents({})))
except Exception as e:
    print("Falha na inserção: {}".format(e))

# indexação para contagem
print("Indexando...")
sleep(2)
try:
    eventos_db.create_index("atualizado_em", expireAfterSeconds = 604800)
    janela_tempo = datetime.now() - timedelta(hours=6)
    pipeline = [
        {"$match": {"atualizado_em": {"$gte": janela_tempo}}},
        {"$group": {"_id": {"$hour": "$atualizado_em"}, "total": {"$sum": 1}}},
        {"$sort": {"_id": 1}}
    ]

except Exception as e:
    print("Indexação falhou: {}".format(e))

print(f"\nOrganizando dados...")
sleep(2)
try:
    resultados = list(eventos_db.aggregate(pipeline))
    if resultados:
        pico = max(resultados, key=lambda x:x['total'])
        hora_pico = pico['_id']
        total_pico = pico['total']

        print(f"\n=== Falhas por hora (ultimas 24h) ===")
        for linha in resultados:
            hora = linha['_id']
            total = linha['total']
            hora_str = "{:02d}h".format(hora)
            barra_grafico = ">" * total

            if hora == hora_pico:
                print("{} | {} {} <- pico".format(hora_str, barra_grafico, total))
            else:
                print("{} | {} {}".format(hora_str, barra_grafico, total))
except Exception as e:
    print("Falha na exibição dos eventos: {}".format(e))

'''
O TTL, além de aprimorar consultas em bancos extensos, e conservar espaço em disco,
ajuda a eliminar registros que já possam ter sido resolvidos, ou até mesmo, irrelevantes,
devido ao tempo, eliminando, nas analises, o risco de falsos positivos, e mantendo
as ocorrencias atuais como relevantes.
'''