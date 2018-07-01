# -*- coding: utf-8 -*-
"""
Created on Fri Dec  8 15:20:09 2017

@author: hpy2
"""

import requests
import json
import hashlib
from pyfiglet import Figlet

def main(filepath, trialchainip):
    url = "http://{0}:9000/trialchain/data_asset".format(trialchainip)
    with open(filepath, 'rb') as f:
        data = f.read()
        hasher = hashlib.md5()
        hasher.update(data)
        md5 = hasher.hexdigest()
    r = requests.get(url, params={"md5": md5, "trialchainip": trialchainip})
    response = r.json()
    f = Figlet(font='slant')
    print(f.renderText('TrialChain'))
    ordered = {
        'asset': response['asset'],
        'sha256': response['sha256'],
        'issuetxid': response['issuetxid'],
        'source': response['source'],
        'issued': response['issued'],
        'validated': response['validated'],
        'ethstatus': response['ethstatus'],
        'confirmations': response['confirmations'],
        'mchash': response['mchash'],
        'ethtxid': response['ethtxid']
    }
    print(json.dumps(ordered, indent=4))
