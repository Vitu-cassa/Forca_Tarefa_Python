# Anotações dos exercicios:
Parece-me uma boa oportunidade de criar uma função mais robusta para conexão com o mongo.
---

## Exercicio 2.1:
1. Interface reciclada do exercicio 3 do CP2 do primeiro semestre.
2. Ainda não descolei uma forma de fazer a conexão ao banco como uma função...
3. O exercicio pode contar com um tratamento de erros personalizado, como a verificação de IPs inválidos.<br>
3.1 Os IPs invalidos podem ser tratados com `indexação`, transferindo essa verificação para o banco. 
> **NOTA:** A indexação foi implementada logo após a criação da coleção. Interessante saber que posso fazer isso antes de populacionar o banco, o que é até obvio. Criar uma função separada para indexação pode ser uma opção.
>
4. Durante as requisições, deixo uma conexão aberta ao banco, enquanto a opção 6 não é escolhida, poderia garantir que cada opção feche a conexão, assim como evocar a fnução `_conexaoMongo()` em cada opção.

---

## Exercicio 2.2:
1. Arquivo `auth.log` criado em `\99-miscelnaea`.
2. Considerar trabalhar com arquivos em diretorios diferentes, para me acostumar com a interação com a arquitetura de arquivos dasd máquinas.
> **NOTA:** Normalizar o arquivo foi osso demais. Tenho que melhorar a interação com arquivos externos.
>
3. Apesar de funcionar, a função retonra apenas o ultimo elemento parseado...<br>
Retiro o que disse, a função não esta criando um dicionario completo...
> Isso ocorre porque não estou fazendo o update do dicionario `resultado` da função `_normalizadorDeLogs()`.
> É melhor abrir e tratar a linha direto na função, ou fora dela, passando-a como parâmetro?
> **DECISÃO:** resolvi tratar as linhas fora e passar como parâmetro. Mas acredito que meu erro foi na hora de retornar o valor, não estava os guardando em uma `lista`.
>

4. Criação do banco e coleção recicladas do exercicio anterior.
5. O exercício ainda pode ficar mais refinado, consideradno um ambiente real, adicionar um tratamento melhor para situações do log, como arquivo em branco e campos não preenchidos. Pode ficar como ponto de melhoria.

---

## Exercicio 2.3:
1. 