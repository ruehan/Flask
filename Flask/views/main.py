from flask import Blueprint, session, g
from flask.json import jsonify
from flask.globals import request
from flask.templating import render_template
from werkzeug.utils import redirect
from models import db, User
import requests


bp = Blueprint('', __name__, url_prefix='')

@bp.route("/test")
def test():
    print(request.form["files"])

    return 0
