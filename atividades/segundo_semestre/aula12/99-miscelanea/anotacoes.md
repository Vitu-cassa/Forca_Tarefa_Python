# Anotações do exercicio:
---
## Exercicio 12.1:
1. Realizei o pipeline com as infomrações ditas no enunciado, a saída foi:
>
> ```python
> estimador:100
> Acurácia: 1.000 (+/- 0.000)
> ```
>
Por curiosidade, realizei o teste de treino com um `for`, para variar os estimadores, de 1 até,aproximadamente, 250, conforme código abaixo:
>
> ```python
> ...Codigo Omitido ...
> for estimador in range(1, 250, 49):
>    
>    pipeline = Pipeline([
>        ("scaler", StandardScaler()),
>        ("classifier", RandomForestClassifier(n_estimators=estimador, random_state=41)),
>    ])
>
>    sleep(3)
>    score = cross_val_score(pipeline, x, y, cv=5)
>    print("estimador:{}\n Acurácia: {:.3f} (+/- {:.3f})".format(estimador, score.mean(), score.std()))
> ```
>
A saída deste teste sempre resulta na mesma acuracia, independentemente dos estimadores utilizados.
>
> ```Python
> estimador:1
> Acurácia: 1.000 (+/- 0.000)
>  estimador:50
> Acurácia: 1.000 (+/- 0.000)
> estimador:99
>  Acurácia: 1.000 (+/- 0.000)
> estimador:148
>  Acurácia: 1.000 (+/- 0.000)
> estimador:197
>  Acurácia: 1.000 (+/- 0.000)
> estimador:246
>  Acurácia: 1.000 (+/- 0.000)
> ```
>
Não parece correto. Verificar se os parâmetros indicados pode ser uma saída. Este comportamento pode atrapalhar o processo de comparação, nos próximos exercicios.

2. utilizando os parametros do exemplo, os valores passam a modificar. Talvez, delcarar `y` do modo como o exercicio pede, pode ser a causa de uma acuracia tão precisa e constante.
> ```Python
> estimador:1
>  Acurácia: 0.785 (+/- 0.072)
> estimador:50
>  Acurácia: 0.875 (+/- 0.079)
> estimador:99
>  Acurácia: 0.890 (+/- 0.066)
> estimador:148
>  Acurácia: 0.890 (+/- 0.060)
> estimador:197
>  Acurácia: 0.895 (+/- 0.053)
> estimador:246
>  Acurácia: 0.905 (+/- 0.051)
> ```
> 

--- 

## Exercicio 12.2
1. Como previsto, todos os modelos apresentam acuracia igual (1.00) no fim do processo.
> ```Python
> # Saida da comparação
> RandomForest: 1.000
> SVM: 1.000
> KNN: 1.000
> ```
>