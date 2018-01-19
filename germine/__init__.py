from .forms import UserLoginForm
from .models import Algorithm, Base, Currency, CurrencyApi, Pool, PoolAddress, PoolApi, User, Wallet
from .poolapi import CryptonoteApi

from .fixtures.initial_data import populate
from .fixtures.loader import load_json

from germine import currency_api

from .rate import Rate

import click 

import flask
from flask import Flask, request, render_template
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy.orm.exc import NoResultFound

from urllib.parse import urlparse, urljoin

import json, os


# Devnote: Bug with SQLAlchemy 12.0, must use a later version
# see: https://github.com/flask-admin/flask-admin/issues/1583#issuecomment-355897231

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('germine.config.Default')


# Flask-SQLAlchemy seems to be a dependence of Flask-Admin
db = SQLAlchemy(app)

# see: https://github.com/mitsuhiko/flask-sqlalchemy/issues/98
Base.metadata.create_all(bind=db.engine)


# Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)


# Flask-Admin
admin = Admin(app, name='adminsite', template_mode='bootstrap3')
admin.add_view(ModelView(Algorithm, db.session))
admin.add_view(ModelView(Currency, db.session))
admin.add_view(ModelView(CurrencyApi, db.session))
admin.add_view(ModelView(Wallet, db.session))
admin.add_view(ModelView(PoolAddress, db.session))
admin.add_view(ModelView(PoolApi, db.session))
admin.add_view(ModelView(Pool, db.session))


# Cached Rate
rate_util = Rate()


# from: http://flask.pocoo.org/snippets/62/
def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc
           

@app.cli.command()
def initial_fixture():
    print("Importing fixture")
    populate(db.session)


@app.cli.command()
@click.argument("filename")
def json_fixture(filename):
    print("Importing json fixture")
    load_json(json.load(open(os.path.join(app.instance_path, filename))), db.session)
    

@app.route("/")
@login_required
def index():
    return "Hello, World!"


@login_manager.user_loader
def load_user(user_id):
    try:
        return db.session.query(User).filter(User.id == int(user_id)).one()
    except NoResultFound:
        return None


@app.route("/login", methods=["GET", "POST"])
def login():
    form = UserLoginForm(request.form)
    error = None

    if request.method == 'POST' and form.validate():
        try:
            matched_user = db.session.query(User).filter(User.login == form.login.data).one()
            if matched_user.authenticate(form.password.data):
                login_user(matched_user)
                flask.flash('Logged in successfully')
                next = flask.request.args.get('next')
                if not is_safe_url(next):
                    return flask.abort(400)
                return flask.redirect(next or flask.url_for('index'))
            else:
                error = "Invalid credentials"
        except NoResultFound:
            error = "Invalid credentials"

    return render_template('login.html', form=form, error=error)


@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return flask.redirect(flask.url_for('login'))


@app.route("/wallets")
def get_wallets():
    wallets = db.session.query(Wallet).filter(Wallet.user == current_user)
    results = []
    for wallet in wallets:
        valuation = "NOT IMPLEMENTED"

        api_row = db.session.query(CurrencyApi).filter(CurrencyApi.currency == wallet.currency).one_or_none()
        if api_row:
            ApiClass = getattr(currency_api, api_row.classname)
            api = ApiClass(api_row.base_url)
            balance = api.get_balance(wallet)
            rate = rate_util.get_rate(wallet.currency.name)
            
            valuation = "Confirmed: {}{unit} / {:.2f}$ | Unconfirmed {}{unit} / {:.2f}$" \
                            .format(balance["balance"], balance["balance"]*rate,
                                    balance["unconfirmed"], balance["unconfirmed"]*rate,
                                    unit=wallet.currency.symbol)

        results.append("{}, valuation: {}".format(wallet, valuation))

    return render_template('list.html',
                           label="Wallets for {}".format(current_user.login),
                           elements=results)


@app.route("/balance-summary/<user>/<pool>")
def balance_summary(user, pool):
    # TODO: query by user
    wallet = db.session.query(Wallet).all()[0]
    pool = db.session.query(Pool).filter(Pool.id==pool).one()
    poolapi = CryptonoteApi(pool.api_base_url)
    return str(poolapi.get_balance(wallet))
