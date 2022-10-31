from flask import Flask
import logging

from . import main

from filter import DatetimeStrForm, Perm, UserStrForm

app = Flask(__name__)

log = logging.getLogger('werkzeug')
log.disabled = True

app.jinja_env.filters["datetimefh"] = DatetimeStrForm.cvtDatetimeFormDeltaH
app.jinja_env.filters["datetimef"] = DatetimeStrForm.cvtDatetimeForm
app.jinja_env.filters["hasAnaly"] = Perm.hasAnaly
app.jinja_env.filters["hasAdmin"] = Perm.hasAdmin
app.jinja_env.filters["boolSimb"] = Perm.cvtBoolSimb
app.jinja_env.filters["genderStr"] = UserStrForm.cvtGenderStr

app.register_blueprint(main.bp)
