import logging


logging.basicConfig(
    filename="app.log",
    encoding="utf-8",
    filemode="a",
    format="{asctime} - {levelname} - {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M",
    level=logging.DEBUG,
)

logger = logging.getLogger("iris_logger")

flask_logger = logging.getLogger("werkzeug")
flask_logger.setLevel(logging.ERROR)
