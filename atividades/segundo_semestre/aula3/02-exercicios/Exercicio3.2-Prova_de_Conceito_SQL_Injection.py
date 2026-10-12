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

from pymongo import MongoClient
from time import sleep
from pymongo import errors