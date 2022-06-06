# -*- coding: utf-8 -*-
"""Arvore_de_decisao.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1qBhcuWYyKfg12-fLr0E5Jfkz3F6NszBR

# **Importar Biblioteca**
"""

import numpy as np
import itertools
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier, export_graphviz # Para arvore de decisão
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from six import StringIO
import pydotplus
import matplotlib.image as mpimg
from IPython.display import Image

"""# **Download do Dataset**"""

!pip3 install wget
!wget https://raw.githubusercontent.com/diogocortiz/Curso-IA-para-todos/master/ArvoreDecis%C3%A3o/dataset_einstein.csv

"""# **Carregar o dataset para dataframe(pandas)**"""

df = pd.read_csv('/content/dataset_einstein.csv', delimiter = ';')
display(df.head())

"""# **Descrição do Dataframe**"""

display(df.info())

"""# **Tratar o dataframe**"""

df = df.dropna() # apaga a linha que tiver pelos menos 1 valor nulo
df = df.drop('Patient ID', axis = 1)
df = df.drop('Patient addmited to regular ward (1=yes. 0=no)', axis = 1)
df = df.drop('Patient addmited to semi-intensive unit (1=yes. 0=no)', axis = 1)
df = df.drop('Patient addmited to intensive care unit (1=yes. 0=no)', axis = 1)
display(df.head())

"""# **Analisar o dataframe**"""

# Saber quantidade que deu positivo ou negativo ao SARS-Cov-2
qntd_categoria = df['SARS-Cov-2 exam result'].value_counts()
print(qntd_categoria)

"""# **Definir features e etiqueta**

Necessario transformar o dataframe para array numpy, que sera o tipo de dado que sera usado no treinamento
"""

# y sera etiqueta
y = df['SARS-Cov-2 exam result'].values # converte para array
display(y)

# x sera a matriz com as features
x = df[['Hemoglobin', 'Leukocytes', 'Basophils', 'Proteina C reativa mg/dL']].values
display(x)

"""# **Dividir o Dataframe para treino e teste**"""

x_train_df, x_test_df, y_train_df, y_test_df = train_test_split(x, y, test_size = 0.2, random_state = 3)

"""# **Treinar o modelo**

tree.DecisionTreeClassifier('O criterio', 'tamanho maximo da arvore')
"""

from sklearn import tree
# Criar um algortimo que sera do tipo arvore de decisão

algortimo_arvore = tree.DecisionTreeClassifier(criterion = 'entropy', max_depth = 5) # Criar a  arvore de decisao

# Treinar o modelo
modelo = algortimo_arvore.fit(x_train_df, y_train_df)

"""# **Visualização da arvore de decisão**

A arvore de decisão pode ser considerada um modelo white box, ou seja, um modelo que podemos entender melhor o que ele aprendeu e como ele decide. Podemos mostrar a arvore para isso
"""

nome_features = ['Hemoglobin', 'Leukocytes', 'Basophils', 'Proteina C reativa mg/dL']
nome_classes = modelo.classes_

# Imagem da arvore
dot_data = StringIO()

# dot_data = tree.export_graphviz(my_tree_one, out_file = None, feature_names = featureNames)
export_graphviz(modelo, out_file = dot_data, filled = True, feature_names = nome_features, class_names = nome_classes, rounded = True, special_characters = True)
grafico = pydotplus.graph_from_dot_data(dot_data.getvalue())
Image(grafico.create_png())
grafico.write_png('arvore.png')
Image('arvore.png')

"""# **Features mais importante para o modelo**"""

importances = modelo.feature_importances_
indices = np.argsort(importances)[::-1]
print('Feature ranking')

for f in range(x.shape[1]):
  print(f'feature {f + 1}, {indices[f]}, {importances[indices[f]]}')
  
f, ax = plt.subplots(figsize = (11, 9))
plt.title('Feature ranking', fontsize = 20)
plt.bar(range(x.shape[1]), importances[indices], color = 'g', align = 'center')
plt.xticks(range(x.shape[1]), indices)
plt.xlim([-1, x.shape[1]])
plt.ylabel('Importance', fontsize = 18)
plt.xlabel('Index of the features', fontsize = 18)
plt.show()

#   Indice das features
''' 0 - Hemoglobin
    1 - Leukocytes
    2 - Basophils
    3 - Proteina C reativa mg/dL '''

"""# **Testar modelo**"""

# Aplicando o modelo na base de dados de teste
y_predicoes_df = modelo.predict(x_test_df)

#Avaliação do modelo
#Vamos avaliar o valor real do dataset y_test_df com as predições
print('Acurácia da arvore: ', accuracy_score(y_test_df, y_predicoes_df).round(2))
print(classification_report(y_test_df, y_predicoes_df))

# precision: das classificações que o modelo fez para uma determinada classe, quantas efetivamente eram correta
# recall: Dos possiveis datapoints pertecentes a uma determinada classe, quantos o modelo conseguiu classificar corretamente

"""# **Matriz de confusão**"""

def plot_confusion_matrix(cm, classes,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Matriz de Confusão Normalizada")
    else:
        print('Matriz de Confusão sem normalizacão ')

    print(cm)

    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, cm[i, j],
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('Rótulo real')
    plt.xlabel('Rótulo prevista')

matrix_confusao = confusion_matrix(y_test_df, y_predicoes_df)
plt.figure()
plot_confusion_matrix(matrix_confusao, classes=nome_classes,
                      title='Matrix de Confusao')