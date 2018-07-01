from flask import render_template, flash, redirect, url_for, request, jsonify
from flask_login import login_required
from app import current_app, db
from app.main import bp
from app.main.forms import AdminForm, EthForm, SearchForm
from app.models import MultichainNode, EthTx
from Savoir import Savoir
from web3 import Web3, HTTPProvider, middleware
from web3.gas_strategies.time_based import fast_gas_price_strategy
from web3.middleware import geth_poa_middleware
from ethereum import transactions, utils
from datetime import datetime
import rlp
import ast
import json
import urllib.request
from urllib.parse import urlparse

@bp.route('/')
@bp.route('/index')
@login_required
def index():
    return render_template('main/index.html', title='Home')

@bp.route('/nodes', methods=['GET', 'POST'])
@login_required
def nodes():
    form = AdminForm()
    if form.submit1.data and form.validate():
        grant = {
            'connect': form.connect.data,
            'send': form.send.data,
            'receive': form.receive.data,
            'issue': form.issue.data
        }
        permissions = ','.join(key for key in grant if grant[key])
        api = Savoir(
            current_app.config['CHAIN_RPC_USER'],
            current_app.config['CHAIN_RPC_PASSWORD'],
            current_app.config['CHAIN_RPC_HOST'],
            current_app.config['CHAIN_RPC_PORT'],
            current_app.config['CHAIN_NAME'])
        api.grant(str(form.address.data), str(permissions))
        node = MultichainNode(
            address=form.address.data,
            connect=form.connect.data,
            send=form.send.data,
            receive=form.receive.data,
            issue=form.issue.data
        )
        db.session.add(node)
        db.session.commit()
        flash('Congratulations, you registered a node on Multichain!')
        return redirect(url_for('main.index'))
    return render_template('main/admin.html', title='Add Node', form=form)

@bp.route('/ethereum', methods=['GET', 'POST'])
@login_required
def ethereum():
    form = EthForm()
    if form.submit2.data and form.validate():
        api = Savoir(
            current_app.config['CHAIN_RPC_USER'],
            current_app.config['CHAIN_RPC_PASSWORD'],
            current_app.config['CHAIN_RPC_HOST'],
            current_app.config['CHAIN_RPC_PORT'],
            current_app.config['CHAIN_NAME']
        )

        url = form.url.data
        if not url:
            url = current_app.config['GETH_URL']
        w3 = Web3(HTTPProvider(url))
        if current_app.config['GETH_MODE'] == 'dev':
            w3.middleware_stack.inject(geth_poa_middleware, layer=0)
            gasPrice = 2000000000
        else:
            gasPrice = w3.eth.gasPrice
            # gasPrice = w3.eth.generateGasPrice()
        privkey = current_app.config['ETH_KEY']
        account = w3.toChecksumAddress(utils.privtoaddr(privkey))
        block_hash = api.getblockchaininfo().get('bestblockhash')

        nonce = w3.eth.getTransactionCount(account)
        startgas = round(w3.eth.estimateGas({'data': block_hash}))
        to = account
        value = 0

        balance = w3.eth.getBalance(account)
        cost = startgas*gasPrice
        if cost > balance:
            flash('Your account has insufficient funds!')
            return redirect(url_for('main.ethereum'))

        tx = transactions.Transaction(nonce, gasPrice, startgas, to, value, block_hash)
        tx.sign(privkey)
        rlp_tx = rlp.encode(tx)
        hex_tx = w3.toHex(rlp_tx)

        response = w3.eth.sendRawTransaction(hex_tx)
        trans = EthTx(
            address=account,
            txid=response,
            mchash=block_hash[2:],
            sent=datetime.now()
        )
        db.session.add(trans)
        db.session.commit()
        flash('Congratulations, you validated the Multichain on Ethereum!')
        return redirect(url_for('main.index'))
    return render_template('main/admin.html', title='Validate TrialChain', form=form)

@bp.route('/assets', methods=['GET', 'POST'])
@login_required
def assets():
    form = SearchForm()
    if form.submit3.data and form.validate():
        md5 = form.md5.data
        return redirect(url_for('main.results', md5=md5))
    return render_template('main/admin.html', title='Check Asset', form=form)

@bp.route('/results')
@login_required
def results():
    md5 = request.args['md5']
    api = Savoir(
        current_app.config['CHAIN_RPC_USER'],
        current_app.config['CHAIN_RPC_PASSWORD'],
        current_app.config['CHAIN_RPC_HOST'],
        current_app.config['CHAIN_RPC_PORT'],
        current_app.config['CHAIN_NAME']
    )
    assets = api.listassets([md5])
    if type(assets) is dict:
        flash('Asset with md5 hash {0} not found!'.format(md5))
        return redirect(url_for('main.assets'))
    else:
        asset = assets[0]
    issued = datetime.fromtimestamp(float(asset['details']['processed.ts'])/1000.0)
    first_eth = EthTx.query.filter(EthTx.sent>issued).order_by('id').first()
    if not first_eth:
        validated = 'Not yet validated'
        ethtxid = 'N/A'
        ethstatus = 'N/A'
        confirmations = 'N/A'
        mchash = 'N/A'
    else:
        validated = first_eth.sent
        ethtxid = first_eth.txid
        mchash = first_eth.mchash
        api = "https://api.blockcypher.com/v1/eth/main/txs/{0}?token={1}".format(ethtxid, current_app.config['BCYPHER_TOKEN'])
        response = urllib.request.urlopen(api)
        txdata = json.loads(response.read().decode('utf-8'))
        if txdata.get("error"):
            ethstatus = 'Invalid/Not Found'
            confirmations = 'N/A'
        elif txdata.get("block_height") == -1:
            ethstatus = 'Pending'
            confirmations = 'N/A'
        else:
            ethstatus = 'Confirmed'
            confirmations = txdata.get("confirmations")
    data = {
        'asset': asset['name'],
        'issuetxid': asset['issuetxid'],
        'issued': issued,
        'validated': validated,
        'ethtxid': ethtxid,
        'ethstatus': ethstatus,
        'confirmations': confirmations,
        'mchash': mchash,
        'source': asset['details']['source.uri'],
        'sha256': asset['details']['hash.sha256']
    }
    return render_template('main/results.html', title='Results', data=data)

@bp.route('/api')
def api():
    md5 = request.args.get('md5')
    api = Savoir(
        current_app.config['CHAIN_RPC_USER'],
        current_app.config['CHAIN_RPC_PASSWORD'],
        current_app.config['CHAIN_RPC_HOST'],
        current_app.config['CHAIN_RPC_PORT'],
        current_app.config['CHAIN_NAME']
    )
    assets = api.listassets([md5])
    if type(assets) is dict:
        data = {"error": "Asset with md5 hash {0} not found!".format(md5)}
        return jsonify(data)
    else:
        asset = assets[0]
    issued = datetime.fromtimestamp(float(asset['details']['processed.ts'])/1000.0)
    first_eth = EthTx.query.filter(EthTx.sent>issued).order_by('id').first()
    if not first_eth:
        validated = 'Not yet validated'
        ethtxid = 'N/A'
        ethstatus = 'N/A'
        confirmations = 'N/A'
        mchash = 'N/A'
    else:
        validated = first_eth.sent
        ethtxid = first_eth.txid
        mchash = first_eth.mchash
        api = "https://api.blockcypher.com/v1/eth/main/txs/{0}?token={1}".format(ethtxid, current_app.config['BCYPHER_TOKEN'])
        response = urllib.request.urlopen(api)
        txdata = json.loads(response.read().decode('utf-8'))
        if txdata.get("error"):
            ethstatus = 'Invalid/Not Found'
            confirmations = 'N/A'
        elif txdata.get("block_height") == -1:
            ethstatus = 'Pending'
            confirmations = 'N/A'
        else:
            ethstatus = 'Confirmed'
            confirmations = txdata.get("confirmations")
    data = {
        'asset': asset['name'],
        'sha256': asset['details']['hash.sha256'],
        'issuetxid': asset['issuetxid'],
        'source': asset['details']['source.uri'],
        'issued': issued,
        'validated': validated,
        'ethstatus': ethstatus,
        'confirmations': confirmations,
        'mchash': mchash,
        'ethtxid': ethtxid
    }
    return jsonify(data)
