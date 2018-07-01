import falcon
import json
import requests
from Savoir import Savoir
import base64
import os
from datetime import datetime

class InterfaceDataAsset(object):
	def on_post(self, req, resp):
		obj = req.context['result']

		rpcuser = os.getenv('CHAIN_RPC_USER')
		rpcpasswd = os.getenv('CHAIN_RPC_PASSWORD')
		rpchost = os.getenv('CHAIN_RPC_HOST')
		rpcport = os.getenv('CHAIN_RPC_PORT')
		chainname = os.getenv('CHAIN_NAME')

		api = Savoir(rpcuser, rpcpasswd, rpchost, rpcport, chainname)

		meta = {}
		for k,v in obj.items():
			meta[k] = v

		owner = api.listpermissions("issue")
		addr_system = owner[0]['address']

		transaction = issue_asset(api, addr_system, obj['hash.md5'], meta)
		resp.body = json.dumps(transaction)

	def on_get(self, req, resp):
		md5 = req.get_param('md5')
		trialchainip = req.get_param('trialchainip')
		url = "http://{0}:5000/api".format(trialchainip)
		response = requests.get(url, params={"md5": md5})
		details = response.json()
		resp.body = json.dumps(details)


class JSONTranslator(object):
    def process_request(self, req, resp):
        # req.stream corresponds to the WSGI wsgi.input environ variable,
        # and allows you to read bytes from the request body.
        #
        # See also: PEP 3333
        if req.content_length in (None, 0):
            # Nothing to do
            return

        body = req.stream.read()
        if not body:
            raise falcon.HTTPBadRequest('Empty request body',
                                        'A valid JSON document is required.')

        try:
            req.context['result'] = json.loads(body.decode('utf-8'))

        except (ValueError, UnicodeDecodeError):
            raise falcon.HTTPError(falcon.HTTP_753,
                                   'Malformed JSON',
                                   'Could not decode the request body. The '
                                   'JSON was incorrect or not encoded as '
                                   'UTF-8.')

    def process_response(self, req, resp, resource):
        if 'result' not in req.context:
            return

        resp.body = json.dumps(req.context['result'])


def max_body(limit):
    def hook(req, resp, resource, params):
        length = req.content_length
        if length is not None and length > limit:
            msg = ('The size of the request is too large. The body must not '
                   'exceed ' + str(limit) + ' bytes in length.')

            raise falcon.HTTPRequestEntityTooLarge(
                'Request body is too large', msg)

    return hook


def issue_asset(api, addr, asset_name, metadata):
	asset_info = {
		"name": asset_name,
		"open": True
	}
	return api.issue(addr, asset_info, 1, 1, 0, metadata)

app = falcon.API(middleware=[JSONTranslator()])

data_asset = InterfaceDataAsset()
app.add_route('/trialchain/data_asset', data_asset)
