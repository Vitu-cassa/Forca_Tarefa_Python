/* +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Exercício 1.3 — Decisão de arquitetura com CAP
    Para cada cenário abaixo, indique se você escolheria um banco CP ou AP e
    justifique em 2 linhas. Entregue como um arquivo decisoes_cap.md.

    Cenários:
    1. Tabela de saldo bancário de clientes.
    2. Ingestão de 500 mil eventos de firewall por minuto num SOC.
    3. Cache de tokens de sessão de usuários logados.
    4. Registro de quem autorizou cada transferência (auditoria).
    5. Feed de indicadores de ameaça (IOCs) replicado em 5 regiões.

    Saída esperada: uma tabela com Cenário | CP/AP | Justificativa.
    Gabarito de referência: 1=CP, 2=AP, 3=AP (ou CP p/ sessões críticas), 4=CP, 5=AP.
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ */

-- DROP TABLE escolha_CAP; --<- Descomentar para novos testes
 
-- Cria tabela para inserir as respostas
 
CREATE TABLE escolha_CAP (
	id INT AUTO_INCREMENT PRIMARY KEY,
	caso VARCHAR(200) NOT NULL,
	tipo ENUM("CA", "CP", "PA"),
	Justificativa VARCHAR(100)
);
 
-- Respostas
 
INSERT INTO escolha_CAP (caso, tipo, justificativa)
VALUES ("Tabela de saldo bancário de clientes","CP", "O saldo precisa ser lido e armazenado com o mesmo valor");
 
INSERT INTO escolha_CAP (caso, tipo, justificativa)
VALUES ("Ingestão de 500 mil eventos de firewall por minuto num SOC", "CA", "Os logs precisam ser armazenados durante um tempo");
 
INSERT INTO escolha_CAP (caso, tipo, justificativa)
VALUES ("Cache de tokens de sessão de usuários logados", "PA", "A sessão não precisa ser armazenada, porem, toda requisição precisa ser respondida");
 
INSERT INTO escolha_CAP (caso, tipo, justificativa)
VALUES ("Registro de quem autorizou cada transferência (auditoria)", "CP", "As transferencias precisam estar armazenadas para consulta");
 
INSERT INTO escolha_CAP (caso, tipo, justificativa)
VALUES ("Feed de indicadores de ameaça (IOCs) replicado em 5 regiões", "CA", "Todos os indicadores devem ser armazenados e replicados ao mesmo tempo");
 
-- Visualiza tabela com respostas
 
SELECT * FROM escolha_CAP;