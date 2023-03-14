""" Lab 10: Save people
You can save people from heart disease by training a model to predict whether a person has heart disease or not.
The dataset is available at src/lab10/heart.csv
Train a model to predict whether a person has heart disease or not and test its performance.
You can usually improve the model by normalizing the input data. Try that and see if it improves the performance.
"""
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import normalize
import pandas as pd
import numpy as np

data = pd.read_csv("src/lab10/heart.csv")

# Transform the categorical variables into dummy variables.
print(data.head())
string_col = data.select_dtypes(include="object").columns
df = pd.get_dummies(data, columns=string_col, drop_first=False)
print(data.head())

y = df.HeartDisease.values
x = df.drop(["HeartDisease"], axis=1)
x_train, x_test, y_train, y_test = train_test_split(
    x, y, test_size=0.2, random_state=25
)

""" Train a sklearn model here. """
sklearn_model = None
sklearn_model = KNeighborsClassifier(n_neighbors=3)
sklearn_model.fit(x,y)
# Accuracy
print("Accuracy of model: {}\n".format(sklearn_model.score(x_test, y_test)))
# accuracy on first run: 82.0% (k=3)

""" Improve the model by normalizing the input data. """
new_x = normalize(x)
new_x_test = normalize(x_test)

model_2 = None
model_2 = KNeighborsClassifier(n_neighbors=3)
model_2.fit(new_x,y)

print("Accuracy of improved model: {}\n".format(model_2.score(new_x_test, y_test)))
# accuracy of second run: 86.4% (k=3)

sklearn_model = None
sklearn_model = KNeighborsClassifier(n_neighbors=2, algorithm='brute')
sklearn_model.fit(x,y)
# Accuracy
print("Accuracy of model: {}\n".format(sklearn_model.score(x_test, y_test)))
#tested other algorithms besides "auto" and didn't get a better accuracy