import os
import sys
import yaml
from aptos_sdk.account_address import AccountAddress

from util.client import RestClient
from util.constant import NODE_URL, RESOURCE_ADDRESS
from util.account import prepareAccount


def create_whitelist():

    with open(os.path.join(sys.path[0], "../.aptos/config.yaml"), 'r') as f:
        config = yaml.safe_load(f)

    _ACCOUNT_ADDRESS = config['profiles']["default"]["account"]
    _ACCOUNT_PRIVATE_KEY = config['profiles']["default"]["private_key"]

    rest_client = RestClient(NODE_URL)
    try:
        alice = prepareAccount(_ACCOUNT_ADDRESS, _ACCOUNT_PRIVATE_KEY)
    except: return
    # accountAddres = (_ACCOUNT_ADDRESS)
    txn_hash = rest_client.create_market(alice,
                                        "Rare Wave Market",
                                        500, # 500 / 10000 = 5%
                                         AccountAddress.from_hex(_ACCOUNT_ADDRESS))

    rest_client.wait_for_transaction(txn_hash)
    print("\n Success, txn hash: " + txn_hash)


create_whitelist()