import argparse
import json
import logging
import os
from checker.main.main import main

class CheckAsset(object):

    def __init__(self):
        self.parser = argparse.ArgumentParser()
        required = self.parser.add_argument_group('required arguments')
        required.add_argument(
            '--filepath',
            help='File Path',
            required=True
        )
        required.add_argument(
            '--trialchainip',
            help='TrialChain IP',
            required=True
        )
        self.parser.add_argument(
            '--verbose',
            action='store_true',
            help='Verbose log output'
        )

    def __call__(self):
        args = self.parser.parse_args()
        if args.verbose:
            logging.basicConfig(level=logging.DEBUG)
        if not os.path.exists(args.filepath):
            raise Exception('requires valid file path')
        main(args.filepath, args.trialchainip)

check_asset = CheckAsset()
