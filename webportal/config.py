import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')  or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    CHAIN_NAME = os.environ.get('CHAIN_NAME') or 'no-multichain-name'
    CHAIN_RPC_USER = os.environ.get('CHAIN_RPC_USER') or 'no-rpc-user'
    CHAIN_RPC_PASSWORD = os.environ.get('CHAIN_RPC_PASSWORD') or 'no-rpc-password'
    CHAIN_RPC_HOST = os.environ.get('CHAIN_RPC_HOST') or 'no-rpc-host'
    CHAIN_RPC_PORT = os.environ.get('CHAIN_RPC_PORT') or 'no-rpc-port'

    ETH_KEY = os.environ.get('ETH_KEY') or 'no-eth-key'
    ETH_ACCOUNT = os.environ.get('ETH_ACCOUNT') or '0xde0B295669a9FD93d5F28D9Ec85E40f4cb697BAe'
    GETH_URL = os.environ.get('GETH_URL') or 'no-geth-url'
    ETHIO_TOKEN = os.environ.get('ETHIO_TOKEN') or 'no-ethio-token'
    BCYPHER_TOKEN = os.environ.get('BCYPHER_TOKEN') or 'no-bcypher-token'
    GETH_MODE = os.environ.get('GETH_MODE') or 'fast'
