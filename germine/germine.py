from .models import Algorithm, Base, Currency, Pool, PoolAddress, PoolApi, Wallet
from .poolapi import CryptonoteApi

from .fixtures.initial_data import populate

from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_sqlalchemy import SQLAlchemy

# Devnote: Bug with SQLAlchemy 12.0, must use a later version
# see: https://github.com/flask-admin/flask-admin/issues/1583#issuecomment-355897231

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('germine.config.Default')

db = SQLAlchemy(app)

# see: https://github.com/mitsuhiko/flask-sqlalchemy/issues/98
Base.metadata.create_all(bind=db.engine)

admin = Admin(app, name='adminsite', template_mode='bootstrap3')
admin.add_view(ModelView(Algorithm, db.session))
admin.add_view(ModelView(Currency, db.session))
admin.add_view(ModelView(Wallet, db.session))
admin.add_view(ModelView(PoolAddress, db.session))
admin.add_view(ModelView(PoolApi, db.session))
admin.add_view(ModelView(Pool, db.session))


@app.cli.command()
def initial_fixture():
    print("Importing fixture")
    populate(db.session)

    
@app.route("/")
def hello_world():
    return "Hello, World!"


@app.route("/balance-summary/<user>/<pool>")
def balance_summary(user, pool):
    # TODO: query by user
    wallet = db.session.query(Wallet).all()[0]
    pool = db.session.query(Pool).filter(Pool.id==pool).one()
    poolapi = CryptonoteApi(pool.api_base_url)
    return str(poolapi.get_balance(wallet))
