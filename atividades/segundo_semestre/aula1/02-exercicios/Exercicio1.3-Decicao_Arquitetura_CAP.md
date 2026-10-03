# Exercício 1.3 — Decisão de arquitetura com CAP
    Para cada cenário abaixo, indique se você escolheria um banco CP ou AP e justifique em 2 linhas. Entregue como um arquivo decisoes_cap.md.

    Cenários:
    1. Tabela de saldo bancário de clientes.
    2. Ingestão de 500 mil eventos de firewall por minuto num SOC.
    3. Cache de tokens de sessão de usuários logados.
    4. Registro de quem autorizou cada transferência (auditoria).
    5. Feed de indicadores de ameaça (IOCs) replicado em 5 regiões.

    Saída esperada: uma tabela com Cenário | CP/AP | Justificativa.
    Gabarito de referência: 1=CP, 2=AP, 3=AP (ou CP p/ sessões críticas), 4=CP, 5=AP.
---

## Tabela de Saldo bacário de Clientes:
**Tipo:** CP (Consistencia e Tolerância a Partições)<br>
**Justificativa:** O saldo precisa ser lido armazenado e armazenado com  o mesmo valor.

## Ingestão de 500 mil Eventos de Firewall por Minuto num SOC
**Tipo:** CA (Consistencia e Disponibilidade)<br>
**Justificativa:** os logs precisam ser armazenados por um bom temppo.

## Cache de Tokens de Sessão de Usuários Logados:
**Tipo:** AP (Disponibilidade e Tolerancia a Partições)<br>
**Justificativa:** A sessão não precisa ser armazenada, porém, toda requisição deve ser respondida.

## Registro de quem Autorizou cada Transferência (auditoria)
**Tipo:** CP (Consistência e Tolerancia a partições)<br>
**Justificativa:** As transferências precisam estar armazenadas para consulta.

## Feed de indicadores de Ameaças (IOCs) Replicado em 5 Regiões:
**Tipo:** CA (Consistencia e Disponibilidade)<br>
**Justificativa:** Todos os indicadores devem ser armazenados e replicados ao  mesmo tempo.