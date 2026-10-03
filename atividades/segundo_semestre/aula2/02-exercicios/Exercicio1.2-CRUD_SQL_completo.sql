/* +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
Exercício 1.2 — CRUD SQL completo
    Escreva os comandos SQL para:
        (a) inserir 3 alertas,
        (b) listar apenas os de severidade 'alta',
        (c) atualizar um alerta para 'resolvido',
        (d) contar alertas por severidade e (e) apagar alertas com mais de 90 dias.

    -- Tabela base:
    CREATE TABLE alertas (
        id INT AUTO_INCREMENT PRIMARY KEY,
        tipo VARCHAR(50), ip_origem VARCHAR(45),
        severidade ENUM('baixa','media','alta','critica'),
        status VARCHAR(20) DEFAULT 'aberto',
        criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    -- Saída esperada (item d):
    -- severidade | total
    -- critica    | 1
    -- alta       | 2
    -- media      | 1
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ */
