from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score

from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import GridSearchCV

import numpy as np


# 12.1 - Por que pipelines
# ++++++++++++++++++++++++++++++++++++++++++++++++

pipeline = Pipeline([
    ("scaler", StandardScaler()),                              # normaliza features
    ("classifier", RandomForestClassifier(n_estimators=100, random_state=42)),
])

X = np.random.RandomState(42).rand(200, 5)
y = (X[:, 0] + X[:, 1] > 1).astype(int)

# Validação cruzada — treina/testa em 5 divisões diferentes e mede a estabilidade
scores = cross_val_score(pipeline, X, y, cv=5)
print(f"Acurácia: {scores.mean():.3f} (+/- {scores.std():.3f})")
# ++++++++++++++++++++++++++++++++++++++++++++++++

# 12.3 Comparando Algoritmos e Ajustando Hiperparamentros
# ++++++++++++++++++++++++++++++++++++++++++++++++
modelos = {
    "RandomForest": RandomForestClassifier(random_state=42),
    "SVM": SVC(),
    "KNN": KNeighborsClassifier(),
}

for nome, modelo in modelos.items():
    scores = cross_val_score(modelo, X, y, cv=5)
    print(f"{nome}: {scores.mean():.3f}")

# GridSearch — testa combinações de hiperparâmetros e escolhe a melhor
grade = {"n_estimators": [50, 100, 200], "max_depth": [None, 5, 10]}
busca = GridSearchCV(RandomForestClassifier(random_state=42), grade, cv=5)
busca.fit(X, y)
print(f"Melhores parâmetros: {busca.best_params_}")
print(f"Melhor score: {busca.best_score_:.3f}")
# ++++++++++++++++++++++++++++++++++++++++++++++++
