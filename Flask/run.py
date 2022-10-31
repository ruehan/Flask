from views import app
from models import db
import os

basdir = os.path.abspath(os.path.dirname(__file__))

dbfile = os.path.join(basdir, 'db.sqlite')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + dbfile

app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SECRET_KEY'] = 'jqiowejrojzxcovnklqnweiorjqwoijroi'

db.init_app(app)
db.app = app
db.create_all()

if __name__ == "__main__":
    app.run(host = '0.0.0.0', port=10001, debug = True)