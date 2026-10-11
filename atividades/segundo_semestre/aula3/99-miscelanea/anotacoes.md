# Anotações dos exercicios:

---

## Exercício 3.1:

1. Menu reciclado do modulo anterior
2. Ainda não faço ideia de como tornar a conexão ao banco como uma função...
> Aparentemente, devo retornar as variáveis de `conexao` e `cursor` da função `_conectorSql()`
>

3. Uma melhoria geral seria criar um diretorio com todas as funções comuns criadas, e importá-las par ao script do exercicio, poupando um tempo de resescrita.
4. O `for` que coloquei para o cadasttro de novo usuário ficou um absurdo (~eu sei que é trivial, mas ainda assim, incrível~). Eu estava na iminência de fazer vários `.append()` para cada campo. Acredito que nos exercicios anteriores eu poderia ter feito igual. =V
5. SQL obriga a usar `lista`, `tupla` ou `dicionario`, mesmo que o parâmetro de busca seja único, portanto, lembrar de "envelopar" o parâmetro em um dos três modelos.
6. Ficar atendo com as quebras de linhas para as queries, elas devem conter cada espaço para separar as isntruções, uma boa prática é, em cada quebra de linha, no fim, adicionar um espaço.
7. Prestar atenção na ordem de envio de parâmetros para as queries, devem seguir, literalmente, a mesma ordem das mascaras.
8. Criar uma função geral para fazer um `drop` de todas as tabelas do banco pode ser útil.
9. Uma melhroia seria realizar a verificação do email cadastrado em cada uma das opções.