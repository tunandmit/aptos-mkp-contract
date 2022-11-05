import os
import sys
import yaml
from aptos_sdk.account_address import AccountAddress

from util.client import RestClient
from util.constant import NODE_URL, RESOURCE_ADDRESS, RESOURCE_MKP_ADDRESS
from util.account import prepareAccount


def create_whitelist():

    with open(os.path.join(sys.path[0], "../.aptos/config.yaml"), 'r') as f:
        config = yaml.safe_load(f)

    _ACCOUNT_ADDRESS = config['profiles']["default"]["account"]
    _ACCOUNT_PRIVATE_KEY = config['profiles']["default"]["private_key"]

    rest_client = RestClient(NODE_URL)
    try:
        alice = prepareAccount('0x7131d840f5197342f71b07f8dd0ecfce17ff05796b709cba0cf529834cba711a',
                               "0xe1118128ad0b86baaa5cae0df0aab47bffffa591e49c31432c2bc7be5a12b99a")
    except: return
    # accountAddres = (_ACCOUNT_ADDRESS)
    txn_hash = rest_client.list_token(alice,
                                        AccountAddress.from_hex(RESOURCE_MKP_ADDRESS),
                                        "Rare Wave Market",
                                        AccountAddress.from_hex(RESOURCE_ADDRESS),
                                        "Rare Wave",
                                        "Rare Wave #0",
                                        0,
                                        1000
                                        )
    rest_client.wait_for_transaction(txn_hash)
    print("\n Success, txn hash: " + txn_hash)


create_whitelist()