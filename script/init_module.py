import os
import sys
import yaml
from util.client import RestClient
from util.constant import NODE_URL
from util.account import prepareAccount


def init_module():

    with open(os.path.join(sys.path[0], "../.aptos/config.yaml"), 'r') as f:
        config = yaml.safe_load(f)

    print(config)
    _ACCOUNT_ADDRESS = config['profiles']["default"]["account"]
    _ACCOUNT_PRIVATE_KEY = config['profiles']["default"]["private_key"]
    print(NODE_URL)
    rest_client = RestClient(NODE_URL)
    try:
        alice = prepareAccount(_ACCOUNT_ADDRESS, _ACCOUNT_PRIVATE_KEY)
    except: return

    txn_hash = rest_client.init_module(alice)
    rest_client.wait_for_transaction(txn_hash)
    print("\n Success, txn hash: " + txn_hash)


init_module()