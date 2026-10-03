/* +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
Exercício 1.2 — CRUD SQL completo
    Escreva os comandos SQL para:
        (a) inserir 3 alertas,
        (b) listar apenas os de severidade 'alta',
        (c) atualizar um alerta para 'resolvido',
        (d) contar alertas por severidade e
        (e) apagar alertas com mais de 90 dias.

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

-- DROP TABLE alertas; -- <- descomentar para novos testes

CREATE TABLE alertas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tipo VARCHAR(50), ip_origem VARCHAR(45),
    severidade ENUM('baixa','media','alta','critica'),
    status VARCHAR(20) DEFAULT 'aberto',
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- insere dados
INSERT INTO alertas (tipo, ip_origem, severidade, status)
    VALUES ("Alerta_1", "192.168.0.4", "alta", "fechado");
INSERT INTO alertas (tipo, ip_origem, severidade, status)
    VALUES ("Alerta_2", "10.10.10.10", "baixa", "aberto");
INSERT INTO alertas (tipo, ip_origem, severidade, criado_em)
    VALUES ("Alerta_3", "255.255.255.255", "alta", "2026-01-01 00:00:00");

-- primeira consulta
SELECT * FROM alertas WHERE severidade = 'alta';

-- atualiza status
UPDATE alertas SET status = 'resolvido' WHERE status = 'fechado';

-- Segundo consulta
SELECT * FROM alertas;

-- contagem de alertas
SELECT severidade,
COUNT(*) AS total
FROM alertas
GROUP BY severidade;

-- Deleta dados antigos

DELETE FROM alertas WHERE criado_em < (NOW() - INTERVAL 90 DAY);
SELECT * FROM alertas
