# Anotações dos exercicios:
Parece-me uma boa oportunidade de criar uma função mais robusta para conexão com o mongo.
---

## Exercicio 2.1:
1. Interface reciclada do exercicio 3 do CP2 do primeiro semestre.
2. Ainda não descolei uma forma de fazer a conexão ao banco como uma função...
3. O exercicio pode contar com um tratamento de erros personalizado, como a verificação de IPs inválidos.<br>
3.1 Os IPs invalidos podem ser tratados com indexação, transferindo essa verificação para o banco.
4. Durante as requisições, deixo uma conexão aberta ao banco, enquanto a opção 6 não é escolhida, poderia garantir que cada opção feche a conexão, assim como evocar a fnução `_conexaoMongo()` em cada opção.
