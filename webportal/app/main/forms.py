from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired
from app import current_app
from app.models import MultichainNode
from web3 import Web3, HTTPProvider
from web3.middleware import geth_poa_middleware
from urllib.parse import urlparse

class AdminForm(FlaskForm):
    address = StringField('Node Address', validators=[DataRequired()])
    connect = BooleanField('Connect')
    send = BooleanField('Send')
    receive = BooleanField('Receive')
    issue = BooleanField('Issue')
    submit1 = SubmitField('Add Node')

    def validate_address(self, address):
        address = MultichainNode.query.filter_by(address=address.data).first()
        if address is not None:
            raise ValidationError('Node is already registered.')

class EthForm(FlaskForm):
    url = StringField('Ethereum API (optional)', description='If API not given, attempts to use local chaindata')
    submit2 = SubmitField('Send Latest Block Hash to Ethereum')

    def validate_url(self, url):
        if url.data:
            parse = urlparse(url.data)
            try:
                parse.scheme
                parse.port
                parse.geturl()
                w3 = Web3(HTTPProvider(parse.geturl()))
                status = w3.eth.syncing
                if status:
                    raise ValidationError('Chaindata is not in sync.')
            except Exception as e:
                raise ValidationError('Invalid URL')
        else:
            try:
                w3 = Web3(HTTPProvider(current_app.config['GETH_URL']))
                if current_app.config['GETH_MODE'] == 'dev':
                    w3.middleware_stack.inject(geth_poa_middleware, layer=0)
                status = w3.eth.syncing
                if status:
                    raise ValidationError('Chaindata is not in sync.')
                elif w3.eth.blockNumber > 50000 and len(w3.admin.peers) == 0:
                    raise ValidationError('No suitable peers found')
            except Exception as e:
                raise ValidationError('{}'.format(str(e)))

class SearchForm(FlaskForm):
    md5 = StringField('Search for Asset by MD5 #', validators=[DataRequired()])
    submit3 = SubmitField('Search')

    def validate_md5(self, md5):
        if md5.data:
            if len(md5.data) != 32:
                raise ValidationError('Invalid MD5 #')
