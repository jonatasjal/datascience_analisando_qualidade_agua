# -*- coding: utf-8 -*-
"""[Jonatas-Liberato] analisando_qualidade_agua.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1YuU-MXO_ZqezkE5ZvZGAgYuNaevvarS1

# **ANALISADO QUALIDADE DE ÁGUA**

Mais um projeto com o objetivo de aprimorar técnicas e neste script serão estados:
- Algoritmos variados de ML
- Imputação de valores missing 
- Padronização de dados

# Problema de Negócio

Todos sabemos que a água é vital para a nossa saúde. Não somente para a nossa saúde, mas para o desenvolvimento da civilização em si.

-

Trata-se de um insumo gratuito usado tanto em nível individual, quanto a nível empresarial.

-

E algo de tanta importância, exige um tratamento adequado, como é o caso do saneamento básico.

-

Políticas públicas que atendam a população de maneira eficiente, geram uma redução no número de doenças e maior qualidade de vida para todos, como é apontado nesse **[estudo](http://www.funasa.gov.br/saneamento-para-promocao-da-saude#:~:text=%C3%81gua%20de%20boa%20qualidade%20para,febre%20tif%C3%B3ide%2C%20esquistossomose%20e%20mal%C3%A1ria.)**.

Além disso, os gastos com o sistema de saúde diminuem, o que proporciona investismentos em outras áreas ou aprimoramento do próprio setor de saúde.
-------

**Objetivo**

Nossa missão é analisar a potabilidade da água com base nas features contidas no dataset.

-------

**Link do Dataset no Kaggle: [AQUI](https://www.kaggle.com/datasets/adityakadiwal/water-potability)**

# Bibliotecas
"""

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd 
import numpy as np 
import seaborn as sns 
import matplotlib.pyplot as plt 
# %matplotlib inline 
import warnings 

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

sns.set_style('darkgrid')
warnings.filterwarnings('ignore')

"""**Dataset**"""

# from google.colab import drive
# drive.mount('/content/drive')

dataset = pd.read_csv('/content/drive/MyDrive/_datasets/water_potability.csv')
dataset

"""Indentificamos que o nosso Target é a variável **Potability**

# 1 - Análise Exploratória
"""

dataset.shape

dataset.describe()

dataset.info()

# Valores nulos
dataset.isnull().sum()

"""*Notamos que existe uma boa quantidade de valores nulos, é onde teremos que fazer uma imputação de valores missing.*"""

dataset['ph'].value_counts()

dataset['ph'].describe()

dataset.nunique()

"""*Para fiz de estudo, vou percorrer os valores dentro do dataset*"""

# Percorrendo os valores dentro do dataset
# Olhando a quantidade (tamanho) do dataset e realizando uma contagem distinta
for column in dataset.columns:
  print('{} possui {} valores únicos'.format(column, len(dataset[column].unique())))

# Analisando o ph da água
dataset['ph'].describe()

"""*Os valores de 6 a 7 representam uma água neutra, não causam efeitos nocivos para a saúde, mas também não proporcionam benefícios. O pH ideal para a nossa saúde é acima de 7. O pH de 7 a 10 significa que a água é alcalina, ou seja, a água ideal para a nossa saúde.*

**Problema**

Ao analisar com mais atenção os dados, notamos uma grande diferença na escala dos dados, para isso, utilizaremos um modelo paramétrico, para normalização/padronização dos dados.

-- 

Vamos plotar um gráfico para melhor visualizar o balanceamento da classe.
"""

# Potability
pot_char = dataset.Potability.value_counts()

# Gráfico de Potability
plt.figure(figsize = (6,3))
sns.barplot(pot_char.index, pot_char)
plt.xlabel('Potability', fontsize = 15)
plt.ylabel('count', fontsize = 20)

"""**Matrix de Correlação**

Muito útil para verificar a relevância das variáveis, para ver se uma não fala a mesma coisa da outra.
"""

# Matrix correlação
plt.figure(figsize = (10, 8))
sns.heatmap(dataset.corr(), annot = True)
plt.title('Matriz de Correlação', fontsize = 20)

"""Aqui vamos criar boxplot e um histograma para analisar a distribuição das variáveis para observarmos outliers.

--

Foi identificado que existem alguns dados inconscientes e mais adiante faremos o tratamento adequado.
"""

# Boxplot
for column in dataset.columns[:-1]:
  plt.figure(figsize = (10,5))
  sns.boxplot(dataset[column])
  plt.title('Boxplot de {}'.format(column), fontsize = 20)

# Histograma
for feature in dataset.columns[:-1]:
  plt.figure(figsize = (10,5))
  sns.histplot(dataset[column], kde = True)
  plt.xlabel(column, fontsize = 15)
  plt.ylabel('count', fontsize = 15)
  plt.title('Histograma de {}'.format(column), fontsize = 20)

"""# 2 - Pré-Processamento"""

# Porcentagem de valores null em cada coluna
for feature in dataset.columns:
  print('{} \t {:.1f}% valores null'.format(feature, (dataset[feature].isnull().sum() / len(dataset)) * 100))

"""**Imputando os valores levando em consideração a média**"""

ph_mean = dataset[dataset['Potability'] == 0]['ph'].mean(skipna=True)
dataset.loc[(dataset['Potability'] == 0) & (dataset['ph'].isna()), 'ph'] = ph_mean

ph_mean_1 = dataset[dataset['Potability'] == 1]['ph'].mean(skipna=True)
dataset.loc[(dataset['Potability'] == 1) & (dataset['ph'].isna()), 'ph'] = ph_mean_1

sulf_mean = dataset[dataset['Potability'] == 0]['Sulfate'].mean(skipna=True)
dataset.loc[(dataset['Potability'] == 0) & (dataset['Sulfate'].isna()), 'Sulfate'] = sulf_mean

sulf_mean_1 = dataset[dataset['Potability'] == 1]['Sulfate'].mean(skipna=True)
dataset.loc[(dataset['Potability'] == 1) & (dataset['Sulfate'].isna()), 'Sulfate'] = sulf_mean_1

traih_mean = dataset[dataset['Potability'] == 0]['Trihalomethanes'].mean(skipna=True)
dataset.loc[(dataset['Potability'] == 0) & (dataset['Trihalomethanes'].isna()), 'Trihalomethanes'] = traih_mean

trah_mean_1 = dataset[dataset['Potability'] == 1]['Trihalomethanes'].mean(skipna=True)
dataset.loc[(dataset['Potability'] == 1) & (dataset['Trihalomethanes'].isna()), 'Trihalomethanes'] = trah_mean_1

dataset.head()

dataset.describe()

"""**Separando variáveis explicativas e target**"""

x = dataset.iloc[:, :-1]
y = dataset.iloc[:, -1]

"""**Criando as amostragens**"""

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size= 0.2, random_state = 0)

"""**Padronizando os dados**
*(calcula o Z)*

- ter um número
- extrair da média
- dividir pelo desvio padrão
"""

# Usando ostandar scaler
sc = StandardScaler()

x_train = sc.fit_transform(x_train)
x_test = sc.fit_transform(x_test)

x_train

x_test

"""# 3 - Criação e avaliação da Máquina Preditiva"""

# Criação do modelo (lista vazia)
modelo_vazio = []

modelos = [LogisticRegression(), KNeighborsClassifier(), RandomForestClassifier(), GaussianNB(), SVC()]

for modelo in modelos:
  modelo.fit(x_train, y_train)
  pred = modelo.predict(x_test)

  modelo_vazio.append(accuracy_score(y_test, pred))

# Resultado em um Dataframe
resultado = pd.DataFrame({
    'Acurácia': modelo_vazio,
    'Nome do Modelo': ['LogisticRegression', 'KNeighborsClassifier', 'RandomForestClassifier', 'GaussianNB', 'SVC'] 
})

resultado

"""**Plotando os resultados.**"""

plt.figure(figsize=(10, 5))
sns.barplot(resultado['Acurácia'], resultado['Nome do Modelo'])
plt.xlabel('Acurácia', fontsize=15)
plt.ylabel('Nome do Modelo', fontsize=15);

"""# Conclusão:

*Um projeto simples onde pudemos trabalhar com análise exploratória, normalização/padronização de dados e trabalho com mais de uma máquina preditiva aplicadas ao mesmo tempo.*
"""

#Autor: Jonatas A. Liberato
#Ref: Eduardo Rocha