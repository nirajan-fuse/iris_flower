import os
from functools import wraps
import logging

import numpy as np
from flask import Flask, request, url_for, redirect, render_template, flash
from pydantic import ValidationError
from dotenv import load_dotenv

from model_training import load_model
from validation import IrisInput

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")

logging.basicConfig(
    filename="app.log",
    encoding="utf-8",
    filemode="a",
    format="{asctime} - {levelname} - {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M",
    level=logging.DEBUG,
)

flask_logger = logging.getLogger("werkzeug")
flask_logger.setLevel(logging.ERROR)

app = Flask(__name__)
app.secret_key = SECRET_KEY

try:
    model = load_model("model.pkl")
    logging.info("Model loaded successfully.")
except FileNotFoundError as e:
    logging.error(e)
    raise SystemExit("Exiting program due to missing model file.")


def validate_iris_input(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            data = IrisInput(
                sepal_length=float(request.form["sepal_length"]),
                sepal_width=float(request.form["sepal_width"]),
                petal_length=float(request.form["petal_length"]),
                petal_width=float(request.form["petal_width"]),
            )
            logging.debug(f"Validated input: {data}")
        except (ValueError, ValidationError) as e:
            for error in e.errors():
                field = error.get("loc", ["unknown"])[0]
                msg = error.get("msg", "Invalid input")

                formatted_messgae = f"{field}: {msg}"
                flash(formatted_messgae)
                logging.warning(f"Validation error: {formatted_messgae}")

            return redirect(url_for("home"))

        return func(*args, **kwargs)

    return wrapper


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/classify", methods=["POST", "GET"])
@validate_iris_input
def classify():
    sepal_length = float(request.form["sepal_length"])
    sepal_width = float(request.form["sepal_width"])
    petal_length = float(request.form["petal_length"])
    petal_width = float(request.form["petal_width"])

    input = np.array([[sepal_length, sepal_width, petal_length, petal_width]])

    output = model.predict(input)
    logging.info(f"Prediction made with input {input}: {output}")

    if output.item() == 0:
        prediction = "Setosa"
    elif output.item() == 1:
        prediction = "Versicolor"
    else:
        prediction = "Virginica"

    logging.debug(f"Prediction result: {prediction}")
    return render_template("home.html", pred=prediction)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)
