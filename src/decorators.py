from flask import request, url_for, redirect, flash
from pydantic import ValidationError

from src.validation import IrisInput
from src.logger_config import logger


def validate_iris_input(func):
    def wrapper(*args, **kwargs):
        try:
            data = IrisInput(
                sepal_length=float(request.form["sepal_length"]),
                sepal_width=float(request.form["sepal_width"]),
                petal_length=float(request.form["petal_length"]),
                petal_width=float(request.form["petal_width"]),
            )
            logger.debug(f"Validated input: {data}")
            return func(data, *args, **kwargs)
        except (ValueError, ValidationError) as e:
            for error in e.errors():
                field = error.get("loc", ["unknown"])[0]
                msg = error.get("msg", "Invalid input")

                formatted_message = f"{field}: {msg}"
                flash(formatted_message)
                logger.warning(f"Validation error: {formatted_message}")

            return redirect(url_for("home"))

    return wrapper
