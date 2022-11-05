import os
import sys
import yaml
from aptos_sdk.account_address import AccountAddress

from util.client import RestClient
from util.constant import NODE_URL,RESOURCE_ADDRESS
from util.account import prepareAccount


def update_winner():

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
    # accountAddres = (_ACCOUNT_ADDRESS)
    txn_hash = rest_client.update_whitelist_info(alice,
                                            AccountAddress.from_hex(RESOURCE_ADDRESS),
                                            1,
                                            AccountAddress.from_hex(_ACCOUNT_ADDRESS),
                                            False,
                                            10000,
                                            1668080752
                                        )
    rest_client.wait_for_transaction(txn_hash)
    print("\n Success, txn hash: " + txn_hash)


update_winner()