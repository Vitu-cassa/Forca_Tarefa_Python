# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
'''Exercício 12.1 — Pipeline de detecção com normalização
        Monte um Pipeline (StandardScaler + classificador) para classificar
        tráfego de rede e avalie com validação cruzada de 5 folds.
        Reporte média e desvio.

        import numpy as np
        X = np.array([
            [500,80,0.1],[1200,80,0.5],[64,22,0.02],[64000,4444,10.0],[45000,8080,15.0],
            [60000,31337,20.0],[800,443,0.3],[300,53,0.05],[55000,9999,18.0],[200,25,0.2],
            [700,443,0.2],[52000,6666,17.0],[150,53,0.03],[58000,4444,19.0],[900,80,0.4],
        ])
        y = np.array([0,0,0,1,1,1,0,0,1,0,0,1,0,1,0])

        # Dica: Pipeline([("scaler",StandardScaler()),("clf",RandomForestClassifier(random_state=42))])
        # Saída esperada (aproximada): Acurácia: ~0.9x (+/- 0.0x)
'''
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score
from time import sleep
import numpy as np

x = np.array([
            [500,80,0.1],[1200,80,0.5],[64,22,0.02],[64000,4444,10.0],[45000,8080,15.0],
            [60000,31337,20.0],[800,443,0.3],[300,53,0.05],[55000,9999,18.0],[200,25,0.2],
            [700,443,0.2],[52000,6666,17.0],[150,53,0.03],[58000,4444,19.0],[900,80,0.4],
        ])

y = np.array([0,0,0,1,1,1,0,0,1,0,0,1,0,1,0])

for estimador in range(1, 250, 49):
    
    pipeline = Pipeline([
        ("scaler", StandardScaler()),
        ("classifier", RandomForestClassifier(n_estimators=estimador, random_state=41)),
    ])

    sleep(3)
    score = cross_val_score(pipeline, x, y, cv=5)
    print("estimador:{}\n Acurácia: {:.3f} (+/- {:.3f})".format(estimador, score.mean(), score.std()))
