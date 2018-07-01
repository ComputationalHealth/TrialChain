from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_socketio import SocketIO
from config import Config
import gevent
from gevent import monkey
from web3 import Web3, HTTPProvider, middleware
from web3.gas_strategies.time_based import fast_gas_price_strategy
from web3.middleware import geth_poa_middleware
import datetime
import requests
import warnings
from functools import wraps

monkey.patch_all()

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'
bootstrap = Bootstrap()
socketio = SocketIO()

def ignore_warnings(f):
    @wraps(f)
    def inner(*args, **kwargs):
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("ignore", category=DeprecationWarning)
            response = f(*args, **kwargs)
        return response
    return inner

@ignore_warnings
def background_thread():
    url = Config.GETH_URL
    account = Config.ETH_ACCOUNT
    token = Config.ETHIO_TOKEN
    test_data = '0x00c2f5cd7c17c548e3106a022fa7632391d46c8e46d285d6a407e6a121a47768'
    peers = 0
    while True:
        gevent.sleep(20)
        now = datetime.datetime.now().strftime("%I:%M:%S")
        try:
            w3 = Web3(HTTPProvider(url))
            market = requests.get('https://api.etherscan.io/api?module=stats&action=ethprice&apikey={0}'.format(token)).json()
            usd = round(float(market.get('result', {}).get('ethusd')))
            ethheight = requests.get('https://api.etherscan.io/api?module=proxy&action=eth_blockNumber&apikey={0}'.format(token)).json()
            height = int(ethheight.get('result'), 16)
            # w3.middleware_stack.add(middleware.time_based_cache_middleware)
            # w3.middleware_stack.add(middleware.latest_block_based_cache_middleware)
            # w3.middleware_stack.add(middleware.simple_cache_middleware)
            # w3.eth.setGasPriceStrategy(fast_gas_price_strategy)
            if Config.GETH_MODE == 'dev':
                w3.middleware_stack.inject(geth_poa_middleware, layer=0)
            status = w3.eth.syncing
        except Exception as e:
            socketio.emit('status', {'data': str(now)+' '+str(e), 'balance': 'Balance: undefined', 'cost': 'TX Cost: undefined'})
            continue
        devmode = True if Config.GETH_MODE == 'dev' else False
        if status:
            status_msg = str(now)+' '+str(status)
        else:
            try:
                local = w3.eth.blockNumber
                peers = len(w3.admin.peers)
                if height - local <= 10 and peers > 0:
                    status_msg = str(now)+' Ethereum ChainData Synced'
                elif height - local <= 10 and peers == 0:
                    status_msg = str(now)+' In-sync, but no suitable peers'
                elif devmode:
                    status_msg = str(now)+' Dev Mode'
                elif height - local > 10 and peers == 0:
                    status_msg = str(now)+' Not syncing, and no suitable peers'
                elif Config.GETH_MODE == 'light':
                    status_msg = str(now)+' Light mode syncing'
            except Exception as e:
                socketio.emit('status', {'data': str(now)+' '+str(e), 'balance': 'Balance: undefined', 'cost': 'TX Cost: undefined'})
                continue
        if peers != 0 or devmode:
            try:
                balance = round(w3.fromWei(w3.eth.getBalance(account), 'ether')*usd, 2)
                if balance == 0 and devmode == False:
                    cost = '?'
                else:
                    startgas = round(w3.eth.estimateGas({'data': test_data}))
                    if devmode:
                        gasPrice = 2000000000
                    else:
                        # gasPrice = w3.eth.generateGasPrice()
                        gasPrice = w3.eth.gasPrice
                    cost = round(w3.fromWei(startgas*gasPrice, 'ether')*usd, 2)
                socketio.emit('status', {'data': status_msg, 'balance': 'Balance: $'+str(balance), 'cost': 'TX Cost: $'+str(cost)})
                continue
            except Exception as e:
                status_msg = str(now)+' '+str(e)
                socketio.emit('status', {'data': status_msg, 'balance': 'Balance: undefined', 'cost': 'TX Cost: undefined'})
                continue
        else:
            socketio.emit('status', {'data': status_msg, 'balance': 'Balance: undefined', 'cost': 'TX Cost: undefined'})
            continue

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    bootstrap.init_app(app)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    socketio.init_app(app)

    bg_task = gevent.spawn(background_thread)

    return app

from app import models
