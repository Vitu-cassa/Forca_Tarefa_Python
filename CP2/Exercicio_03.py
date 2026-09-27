
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
''' Exercício 3 — Retenção e janela temporal (Aula 2):
        Um SOC não guarda log para sempre nem olha o total — olha a janela.
        Crie a coleção eventos com um índice TTL, popule 200 eventos espalhados
        em 24 horas e produza, por agregação, a distribuição de falhas por hora do dia.

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
