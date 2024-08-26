from flask import Flask, request, url_for, redirect, render_template, flash
import pandas as pd
import numpy as np
import pickle
from model_training import load_model

app = Flask(__name__)
app.secret_key = "a76d51c947e7fb2e1a265906ad475761"

model = load_model("model.pkl")


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/classify", methods=["POST", "GET"])
def classify():
    sepal_length = float(request.form["sepal_length"])
    sepal_width = float(request.form["sepal_width"])
    petal_length = float(request.form["petal_length"])
    petal_width = float(request.form["petal_width"])

    if not (4.0 <= sepal_length <= 8.0):
        flash("Sepal length must be between 4.0 and 8.0 cm.")
        return redirect(url_for("home"))
    if not (2.0 <= sepal_width <= 4.5):
        flash("Sepal width must be between 2.0 and 4.5 cm.")
        return redirect(url_for("home"))
    if not (1.0 <= petal_length <= 7.0):
        flash("Petal length must be between 1.0 and 7.0 cm.")
        return redirect(url_for("home"))
    if not (0.1 <= petal_width <= 2.5):
        flash("Petal width must be between 0.1 and 2.5 cm.")
        return redirect(url_for("home"))

    input = np.array([[sepal_length, sepal_width, petal_length, petal_width]])

    output = model.predict(input)

    if output.item() == 0:
        return render_template("home.html", pred="Setosa")
    elif output.item() == 1:
        return render_template("home.html", pred="Versicolor")
    else:
        return render_template("home.html", pred="Virginica")


if __name__ == "__main__":
    app.run(debug=True)
