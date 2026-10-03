/* +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
Exercício 1.1 — Modelagem de banco de vulnerabilidades
    Projete (em papel ou em um arquivo .sql) o schema de um banco relacional para
    gerenciar vulnerabilidades. Deve conter, no mínimo, as tabelas ativos,
    vulnerabilidades e uma tabela de relacionamento ativo_vulnerabilidade.
    Defina PKs, FKs e tipos de coluna.

    -- Dicas de implementação:
    -- ativos: id, nome, ip, tipo, criticidade
    -- vulnerabilidades: id, cve_id, descricao, severidade (ENUM), cvss (DECIMAL)
    -- ativo_vulnerabilidade: ativo_id (FK), vuln_id (FK), status, detectada_em

    -- Saída esperada: um script CREATE TABLE válido que rode sem erros no MySQL.
    -- Teste inserindo: ativo "SRV-WEB01" com a CVE-2024-001 (severidade Alta, cvss 8.5).
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ */

-- DROP TABLE ativos_vulnerabilidades ,ativos, vulnerabilidades <- Descomentar para novo teste

-- Cria tabelas primarias

CREATE TABLE ativos (
	id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(50),
    ip VARCHAR(39) UNIQUE,
    tipo VARCHAR(25),
    criticidade DECIMAL(4, 2),
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE vulnerabilidades(
    id INT AUTO_INCREMENT PRIMARY KEY,
    cve_id VARCHAR(50) UNIQUE,
    descricao VARCHAR(200),
    tipo VARCHAR(25),
    severidade ENUM('baixa', 'media', 'alta', 'critica'),
    cadastrado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insere dados de exemplo nas tabelas
INSERT INTO ativos (nome, ip, criticidade)
    VALUES('SRV-WEB01', '203.0.113.240', 3.7);
    
INSERT INTO vulnerabilidades (cve_id, descricao, severidade)
    VALUES ("CVE-2024-001", "Lorem ipsum dolor sit amet", "critica");

-- cria tabela de juncao

CREATE TABLE ativos_vulnerabilidades(
    id INT PRIMARY KEY,
    ativo_id INT,
    vuln_id INT,
    status ENUM('resolvido', 'aberto', 'so deus na causa'),
    detectada_em TIMESTAMP

    CONSTRAINT fk_ativos,
        FOREIGN KEY (ativo_id)
        REFERENCES ativos(id),
    
    CONSTRAINT fk_vulnerabilidades
        FOREIGN KEY (vuln_id)
        REFERENCES vulnerabilidades(id),
)

-- 