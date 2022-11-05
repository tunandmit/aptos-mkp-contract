from .constant import MODE, FAUCET_URL
from aptos_sdk.account import Account, AccountAddress, ed25519
from pick import pick
from aptos_sdk.client import FaucetClient


def prepareAccount(_ACCOUNT_ADDRESS, _ACCOUNT_PRIVATE_KEY):
    accountAddress = AccountAddress.from_hex(_ACCOUNT_ADDRESS)
    privateKey = ed25519.PrivateKey.from_hex(_ACCOUNT_PRIVATE_KEY)
    alice = Account(accountAddress, privateKey)
    print(f'Public key: {alice.address()}')
    print(f'Private key: {alice.private_key}')

    return alice