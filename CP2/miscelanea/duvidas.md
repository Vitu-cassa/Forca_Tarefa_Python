# 🐍 Arquivo para registrar observações e dúvidas durante a atividade

---
## Exercício 1:
1. Esse primeiro aqui eu, sinceramente, não compreendi. Eu achei que teriam algumas estruturas de `if/elses`, mas o exercício pede para não ter estas condições soltas no código... Entendo o que ele deseja, mas não tô concebendo como realizar o diagnostico sem condicioais.
Talvez ele queira dizer que as condições não devam ficar no programa principal...

2. Qual a melhor forma de fomratar um dicionario ou lista, para ficar legivel no codigo?

3. Eu ainda tenho muita dificildade com `tupplas` e `dicionários`. 

4. Esse foi dose, demorei um tempão para estruturar. Mas apliquei aqui a maior parte de tradução pythonica possível. Estou voltando a tentar estruturar tudo em funções especificas. Adiconalmente, devo prestar mais atenção à formatações de saídas.

**Nota:** A partir daqui, considerando muito em vibe-codar T.T

---

## Exercicio 2:
1. Para criar as novas tabelas, tive que garantir que as antigas fossem removidas. Para estes processos, descobri que o `.executemany()` não serve para criar ou deletar tabelas. pode ser interessante ter um `for` para mais de duas tabelas, na proxima;
> ```python
> tabelas_para_deletar = ['ativos', 'alertas', 'usuarios']
> for tabela in tabelas_para_deletar:
>    cursor.execute("DROP TABLE IF EXISTIS {}".format(tabela))
>```

2. Lidar com as chaves foi dificil. Para deletar uma tabela com `DROP`, deve-se apagar todas as tabelas que herdam caracteristicas antes da tabela "mãe", quanto para o `CREATE`, gera-se a tabela "mãe" primeiro, o que faz bastante sentido.

3. Não consegui transformar a conexão ao banco em uma função... =|

4. Acho que as contagens dos alertas para comparação nao foram feitas da firma mais sofisticada.

5. No meio do caminho, quando fui interagir com o `MongoDB`, acabei não adotando as formas de funções especificas. O codigo poderia ser refatorado com essa funcionabilidade. Além disso, a contagem, principalmente no `mongoDB` pode ser refeita, para um valor mais confiável.

6. Continuo sem entender a relação da instrução `.fetchall()`, por hora, só aceito que ela esteja funcionando.

---

## Exercicio 3:

1. Posso utilizar o gerador de eventos do CP anterior para fazer os eventos com datas aleatorias.
2. Como devo conseguir fazer aquelas barrinhas gráficas?
3. Estruturas de criação de coleções também reaproveitadas de outros exercicios. Ela importa, também outra pratica que eu deveria voltar a fazer, definição de funções especificas para ações especificas.


---

# Apagar templates de formatação

## Saidas de terminal e trechos de codigo
> 
> ```python
> cursor.executemany("INSERT INTO users (nome, email) VALUES (%s, %s)", usuarios)
> ```

> ```python
> # ...saída omitida...
> # Previsões e avaliações
> previsoes = modelo.predict(x_test)
> print("\nAcurácia: {:.2f}".format(accuracy_score(y_test, previsoes)))
> # ...saída omitida...
> ```

## Descrição de passo a passo especifico
> * Enviei uma lista de IPs genéricos para utilização.
> * Solicitei que ela estruturasse um loop com um preenchimento básico de uma lista.
> * Adicionei uma condição para verificar se o contador do loop era par ou ímpar, para inserir um valor diferente para o índice `tipo` da coleção que pretendia usar.
> * Baseado nessa decisão, solicitei que a IA fizesse uma condição para verificar se o contador é primo e, caso seja, colocar em `tipo` o valor de `SUSPEITO`.
> * Solicitei a inserção de uma simulação de data e hora aleatórios.
> * Transformei tudo em uma função chamada `geraEventos()`.
> * A IA sugeriu passar um parâmetro para a função, podendo controlar a quantidade de eventos gerados.
> * A função retorna uma lista com os eventos preenchidos. Utilizo esse retorno para a variável `eventos`, para preenchimento da coleção.
> * Espero, sinceramente, que funcione bem...

