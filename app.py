import os

import numpy as np
from flask import Flask, render_template
from dotenv import load_dotenv

from src.model_training import load_model
from src.decorators import validate_iris_input
from src.logger_config import logger

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")

app = Flask(__name__)
app.secret_key = SECRET_KEY

try:
    model = load_model("model.pkl")
    logger.info("Model loaded successfully.")
except FileNotFoundError as e:
    logger.error(e)
    raise SystemExit("Exiting program due to missing model file.")


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/classify", methods=["POST", "GET"])
@validate_iris_input
def classify(data):
    input = np.array(
        [[data.sepal_length, data.sepal_width, data.petal_length, data.petal_width]]
    )

    output = model.predict(input)
    logger.info(f"Prediction made with input {input}: {output}")

    prediction = ["Setosa", "Versicolor", "Virginica"][output.item()]

    logger.debug(f"Prediction result: {prediction}")
    return render_template("home.html", pred=prediction)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)
