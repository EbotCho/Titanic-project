# -*- coding: utf-8 -*-
"""titanic2(진행중).ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1NpJrgX3LngFzJ-Ai1oO8hLtmREVnehDg
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(font_scale = 2.5)
import missingno as msno
import warnings
warnings.filterwarnings("ignore")

df_gender = pd.read_csv('../content/drive/MyDrive/titanic/gender_submission.csv')
df_train = pd.read_csv('../content/drive/MyDrive/titanic/train.csv')
df_test = pd.read_csv('../content/drive/MyDrive/titanic/test.csv')

columns = ['Pclass', 'Age', 'SibSp', 'Parch', 'Fare', 'Survived', 'Sex']

plt.figure(figsize=(10, 8))

#결손값 확인
for col in df_train.columns:
    msg = 'column: {:>10}\t Percent of NaN value: {:.2f}%'.format(col, 100 * (df_train[col].isnull().sum() / df_train[col].shape[0]))
    print(msg)

# Null 확인
print("counts of missing calue (train) =>", df_train["Embarked"].isnull().sum())
print("-----------------------------------")
print(df_train['Embarked'].value_counts())
print("-----------------------------------\n")
print("counts of missing value(test) => ", df_test["Embarked"].isnull().sum())
print("-----------------------------------")
print(df_test["Embarked"].value_counts())
print("-----------------------------------")

# Embarked열 Null 채우기
df_train["Embarked"].fillna("S", inplace = True)

# Embarked 지역 숫자 mapping
embarked_mapping = {"S":1,"C":2,"Q":3}
df_train["Embarked"] = df_train["Embarked"].map(embarked_mapping).astype(int)

df_test["Embarked"] = df_test["Embarked"].map(embarked_mapping).astype(int)

print("counts of missing calue (train) =>", df_train["Embarked"].isnull().sum())
print("-----------------------------------")
print(df_train['Embarked'].value_counts())
print("-----------------------------------\n")

print("counts of missing value(test) => ", df_test["Embarked"].isnull().sum())
print("-----------------------------------")
print(df_test["Embarked"].value_counts())
print("-----------------------------------")

# Age의 결손값 확인
# df_train["Age"] = df_train["Age"].fillna(df_train["Age"].median())
# df_test["Age"] = df_test["Age"].fillna(df_test["Age"].median())


print("counts of missing calue (train) =>", df_train["Age"].isnull().sum())
print("-----------------------------------")
print(df_train['Age'].value_counts())
print("-----------------------------------\n")

print("counts of missing calue (test) =>", df_test["Age"].isnull().sum())
print("-----------------------------------")
print(df_test['Age'].value_counts())
print("-----------------------------------\n")

df_train["Age2"] = df_train["Age"].fillna(df_train["Age"].median())

df_train['Age2']=pd.cut(df_train['Age'], 8)
df_train.groupby('Age2', as_index=False)['Survived'].mean().sort_values(by="Age2", ascending=True)

df_train['Age2'] = pd.cut(df_train["Age"], bins = 8, labels = [0, 1, 2, 3, 4, 5, 6, 7])
df_train.groupby('Age2', as_index=False)['Survived'].mean().sort_values(by="Age2", ascending=True)

df_test.loc[                        (df_test['Age'] <= 10),   "Age2"] = 0
df_test.loc[(df_test['Age'] > 10) & (df_test['Age'] <= 20),   "Age2"] = 1
df_test.loc[(df_test['Age'] > 20) & (df_test['Age'] <= 30),   "Age2"] = 2
df_test.loc[(df_test['Age'] > 30) & (df_test['Age'] <= 40),   "Age2"] = 3
df_test.loc[(df_test['Age'] > 40) & (df_test['Age'] <= 50),   "Age2"] = 4
df_test.loc[(df_test['Age'] > 50) & (df_test['Age'] <= 60),   "Age2"] = 5
df_test.loc[(df_test['Age'] > 60) & (df_test['Age'] <= 70),   "Age2"] = 6
df_test.loc[(df_test['Age'] > 70),                            "Age2"] = 7

# 성별 맵핑
Gender = {"male":1,"female":2}
df_train["Sex"] = df_train["Sex"].map(Gender).astype(int)

df_test["Sex"] = df_test["Sex"].map(Gender).astype(int)

print("counts of missing calue (train) =>", df_train["Sex"].isnull().sum())
print("-----------------------------------")
print(df_train['Sex'].value_counts())
print("-----------------------------------\n")

print("counts of missing value(test) => ", df_test["Sex"].isnull().sum())
print("-----------------------------------")
print(df_test["Sex"].value_counts())
print("-----------------------------------")

# 가족
df_train['Family'] = df_train['SibSp'] + df_train['Parch'] + 1
df_test['Family'] = df_test['SibSp'] + df_test['Parch'] + 1

df_train.groupby('Family', as_index=False)['Survived'].mean().sort_values(by='Family')

df_train['Alone']=0
df_train.loc[df_train['Family'] == 1, "Alone"] = 1

df_test['Alone']=0
df_test.loc[df_test['Family'] == 1, "Alone"] = 1

df_train.groupby('Alone', as_index=False)['Survived'].mean()

# 요금 
df_train['Fare2'] = pd.qcut(df_train['Fare'], q=5)
df_train.groupby('Fare2', as_index=False)['Survived'].mean().sort_values(by="Fare2", ascending = True)

df_train['Fare2'] = pd.qcut(df_train['Fare'], q = 5, labels=[0, 1, 2, 3, 4])
df_train.groupby('Fare2', as_index=False)['Survived'].mean().sort_values(by='Fare2', ascending = True)

df_test['Fare'].fillna(df_test['Fare'].dropna().median(), inplace = True)

df_test.loc[                             (df_test['Fare'] <= 7.854),   "Fare2"] = 0
df_test.loc[(df_test['Fare'] > 7.854) &  (df_test['Fare'] <= 10.500),   "Fare2"] = 1
df_test.loc[(df_test['Fare'] > 10.5) &   (df_test['Fare'] <= 21.679),   "Fare2"] = 2
df_test.loc[(df_test['Fare'] > 21.679) & (df_test['Fare'] <= 39.688),   "Fare2"] = 3
df_test.loc[(df_test['Fare'] > 39.688),                                 "Fare2"] = 4

df_train.head()

# 딥러닝 학습에 필요한 label / feature 정의

label_column = ['Survived']

feature_columns = ['Pclass', 'Sex', 'Age', 'SibSp', 'Parch', 'Fare', 'Embarked', 'Age2', 'Family', 'Alone', 'Fare2']

train_feature_df = df_train[feature_columns]
test_feature_df = df_test[feature_columns]
train_label_df = df_train[label_column]

print('train shape = ', train_feature_df.shape, ', test shape = ', test_feature_df.shape)

train_feature_df.head(2)

from sklearn.preprocessing import StandardScaler

feature_columns = [ 'Pclass', 'Sex', 'Age', 'SibSp', 'Parch', 'Fare', 'Embarked', 'Age2', 'Family', 'Alone', 'Fare2' ]
# z-score
scaler = StandardScaler()

#train_feature_df 표준화
train_feature_df_scaled = scaler.fit_transform(train_feature_df[feature_columns])
# scaler.fit의 return 값은 numpy 이므로 표준화를 시행한 후 다시 Dataframe 생성 
train_feature_df_scaled = pd.DataFrame(train_feature_df_scaled, columns=feature_columns)

#test_feature_df 표준화
test_feature_df_scaled = scaler.fit_transform(test_feature_df[feature_columns])
test_feature_df_scaled = pd.DataFrame(test_feature_df_scaled, columns=feature_columns)

x_train = train_feature_df_scaled.to_numpy().astype('float32')
x_test = test_feature_df_scaled.to_numpy().astype('float32')
y_train = train_label_df.to_numpy().astype('float32')

print('x_train.shape=', x_train.shape, ', x_test.shape=' ,x_test.shape,' ,y_train.shape =', y_train.shape)

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import SGD, Adam

kaggle_titanic_ann_model = Sequential()

kaggle_titanic_ann_model.add(Dense(64, activation='sigmoid', input_shape=(x_train.shape[1],)))
kaggle_titanic_ann_model.add(Dropout(0.25))
kaggle_titanic_ann_model.add(Dense(2, activation='softmax'))

kaggle_titanic_ann_model.compile(optimizer=SGD(), loss='sparse_categorical_crossentropy', metrics=['accuracy'])

hist = kaggle_titanic_ann_model.fit(x_train, y_train, epochs=200)

survived_prediction = kaggle_titanic_ann_model.predict(x_test)
print(survived_prediction.shape)

from google.colab import files

survived_prediction_digit = np.argmax(survived_prediction, axis=1)
df_gender['Survived'] = survived_prediction_digit
df_gender.to_csv('kaggle_Titanic_Competition.csv', index = False)
files.download('kaggle_Titanic_Competition.csv')

