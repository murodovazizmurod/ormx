import logging
import os

from flask import Flask
from werkzeug.serving import WSGIRequestHandler

app = Flask(__name__, static_folder='assets', template_folder='pages')

# set logging
werkzeug_logger = logging.getLogger('werkzeug')
WSGIRequestHandler.log = lambda self, type, message, *args: \
    getattr(werkzeug_logger, type)('')


@app.route("/")
def hello():
    return "Hello World!"


if __name__ == "__main__":
    app.run(debug=False)
    os.system('cls')
