from flask import Flask
import logging

from . import main

app = Flask(__name__)

log = logging.getLogger('werkzeug')
log.disabled = True

app.register_blueprint(main.bp)
