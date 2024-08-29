import numpy as np
import pandas as pd
import pickle
from sklearn import datasets
from sklearn.linear_model import LogisticRegression


def train_iris_model():
    iris = datasets.load_iris()
    X = iris.data
    y = iris.target

    model = LogisticRegression(max_iter=200)
    model.fit(X, y)

    acc = model.score(X, y)
    print(acc)
    return model


def save_model(model, model_name="model.pkl"):
    file_path = "./model/" + model_name
    pickle.dump(model, open(file_path, "wb"))


def load_model(model_name="model.pkl"):
    file_path = "./model/" + model_name
    loaded_model = pickle.load(open(file_path, "rb"))
    return loaded_model


if __name__ == "__main__":
    iris_model = train_iris_model()
    save_model(iris_model)
