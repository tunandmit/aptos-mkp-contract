import time
from typing import Any, Dict, List, Optional

import httpx

from aptos_sdk.account import Account
from aptos_sdk.account_address import AccountAddress

from aptos_sdk.bcs import Serializer
from aptos_sdk.type_tag import TypeTag, StructTag
from .transactions import (EntryFunction, TransactionPayload)
from aptos_sdk.transactions import (RawTransaction,SignedTransaction, TransactionArgument)
from aptos_sdk.authenticator import (Authenticator, Ed25519Authenticator)
from aptos_sdk import client
from .constant import GAS_UNIT, MAX_GAS, CONTRACT_ADDRESS, MKP_ADDRESS


class RestClient(client.RestClient):
    """A wrapper around the Aptos-core Rest API"""

    chain_id: int
    client: httpx.Client
    base_url: str

    def __init__(self, base_url: str):
        super().__init__(base_url)

    def create_single_signer_bcs_transaction(
            self, sender: Account, payload: TransactionPayload
    ) -> SignedTransaction:
        raw_transaction = RawTransaction(
            sender.address(),
            self.account_sequence_number(sender.address()),
            payload,
            MAX_GAS,
            GAS_UNIT,
            int(time.time()) + 600,
            self.chain_id,
            )

        signature = sender.sign(raw_transaction.keyed())
        authenticator = Authenticator(
            Ed25519Authenticator(sender.public_key(), signature)
        )
        return SignedTransaction(raw_transaction, authenticator)

    def init_module(self, account : Account) -> str:
        payload = EntryFunction.natural(
            CONTRACT_ADDRESS,
            "init_rarewave",
            [],
            []
        )

        signed_transaction = self.create_single_signer_bcs_transaction(
            account, TransactionPayload(payload)
        )
        return self.submit_bcs_transaction(signed_transaction)

    def create_whitelist(self,
                         account : Account,
                         resource_addr: AccountAddress,
                         royalty_payee_address: AccountAddress,
                         paused: bool,
                         price: float,
                         end_time: int) -> str:

        transaction_arguments = [
            TransactionArgument(resource_addr, Serializer.struct),
            TransactionArgument(royalty_payee_address, Serializer.struct),
            TransactionArgument(paused, Serializer.bool),
            TransactionArgument(price, Serializer.u64),
            TransactionArgument(end_time, Serializer.u64),
        ]
        payload = EntryFunction.natural(
            CONTRACT_ADDRESS,
            "create_whitelist",
            [],
            transaction_arguments
        )
        signed_transaction = self.create_single_signer_bcs_transaction(
            account, TransactionPayload(payload)
        )
        return self.submit_bcs_transaction(signed_transaction)

    def update_whitelist_info(self,
                         account : Account,
                         resource_addr: AccountAddress,
                         phase : int,
                         royalty_payee_address: AccountAddress,
                         paused: bool,
                         price: float,
                         end_time: int) -> str:

        transaction_arguments = [
            TransactionArgument(resource_addr, Serializer.struct),
            TransactionArgument(phase, Serializer.u64),
            TransactionArgument(royalty_payee_address, Serializer.struct),
            TransactionArgument(paused, Serializer.bool),
            TransactionArgument(price, Serializer.u64),
            TransactionArgument(end_time, Serializer.u64),
        ]
        payload = EntryFunction.natural(
            CONTRACT_ADDRESS,
            "update_whitelist_info",
            [],
            transaction_arguments
        )
        signed_transaction = self.create_single_signer_bcs_transaction(
            account, TransactionPayload(payload)
        )
        return self.submit_bcs_transaction(signed_transaction)

    def join_whitelist(self,
                       joinner: Account,
                       resource_addr: AccountAddress) -> str:
        transaction_arguments = [
            TransactionArgument(resource_addr, Serializer.struct),
        ]
        payload = EntryFunction.natural(
            CONTRACT_ADDRESS,
            "join_whitelist",
            [],
            transaction_arguments
        )
        signed_transaction = self.create_single_signer_bcs_transaction(
            joinner, TransactionPayload(payload)
        )
        print(signed_transaction)
        return self.submit_bcs_transaction(signed_transaction)

    def claim_nft(self,
                       joinner: Account,
                       resource_addr: AccountAddress) -> str:
        transaction_arguments = [
            TransactionArgument(resource_addr, Serializer.struct),
        ]
        payload = EntryFunction.natural(
            CONTRACT_ADDRESS,
            "claim_nft",
            [],
            transaction_arguments
        )
        signed_transaction = self.create_single_signer_bcs_transaction(
            joinner, TransactionPayload(payload)
        )

        return self.submit_bcs_transaction(signed_transaction)

    def claim_back_aptos(self,
                       joinner: Account,
                       resource_addr: AccountAddress) -> str:
        transaction_arguments = [
            TransactionArgument(resource_addr, Serializer.struct),
        ]
        payload = EntryFunction.natural(
            CONTRACT_ADDRESS,
            "claim_back_aptos",
            [],
            transaction_arguments
        )
        signed_transaction = self.create_single_signer_bcs_transaction(
            joinner, TransactionPayload(payload)
        )

        return self.submit_bcs_transaction(signed_transaction)

    def update_winner(self,
                       joinner: Account,
                       resource_addr: AccountAddress,
                       pharse: int,
                       winner_addr: list,
                       winner_num_nft: list,
                       ) -> str:
        transaction_arguments = [
            TransactionArgument(resource_addr, Serializer.struct),
            TransactionArgument(pharse, Serializer.u64),
            TransactionArgument(winner_addr, Serializer.sequence_serializer(Serializer.struct)),
            TransactionArgument(winner_num_nft, Serializer.sequence_serializer(Serializer.u64)),
        ]
        payload = EntryFunction.natural(
            CONTRACT_ADDRESS,
            "update_winner",
            [],
            transaction_arguments
        )
        signed_transaction = self.create_single_signer_bcs_transaction(
            joinner, TransactionPayload(payload)
        )

        return self.submit_bcs_transaction(signed_transaction)

    def create_market(self,
                       sender: Account,
                       market_name: str,
                       fee_numerator: int,
                       fee_payee: AccountAddress,
                       ) -> str:
        transaction_arguments = [
            # TransactionArgument(sender, Serializer.struct),
            TransactionArgument(market_name, Serializer.str),
            TransactionArgument(fee_numerator, Serializer.u64),
            TransactionArgument(fee_payee, Serializer.struct),
        ]

        payload = EntryFunction.natural(
            MKP_ADDRESS,
            "create_market",
            [
                TypeTag(StructTag.from_str("0x1::aptos_coin::AptosCoin"))
            ],
            transaction_arguments
        )
        signed_transaction = self.create_single_signer_bcs_transaction(
            sender, TransactionPayload(payload)
        )

        return self.submit_bcs_transaction(signed_transaction)

    def list_token(self,
                       seller: Account,
                       market_address: AccountAddress,
                       market_name: str,
                       creator: AccountAddress,
                       collection: str,
                       name: str,
                       property_version: int,
                       price: int,
                       ) -> str:
        transaction_arguments = [
            # TransactionArgument(sender, Serializer.struct),
            TransactionArgument(market_address, Serializer.struct),
            TransactionArgument(market_name, Serializer.str),
            TransactionArgument(creator, Serializer.struct),
            TransactionArgument(collection, Serializer.str),
            TransactionArgument(name, Serializer.str),
            TransactionArgument(property_version, Serializer.u64),
            TransactionArgument(price, Serializer.u64),
        ]

        payload = EntryFunction.natural(
            MKP_ADDRESS,
            "list_token",
            [
                TypeTag(StructTag.from_str("0x1::aptos_coin::AptosCoin"))
            ],
            transaction_arguments
        )
        signed_transaction = self.create_single_signer_bcs_transaction(
            seller, TransactionPayload(payload)
        )

        return self.submit_bcs_transaction(signed_transaction)

    def buy_token(self,
                   seller: Account,
                   market_address: AccountAddress,
                   market_name: str,
                   creator: AccountAddress,
                   collection: str,
                   name: str,
                   property_version: int,
                   price: int,
                   ) -> str:
        transaction_arguments = [
            # TransactionArgument(sender, Serializer.struct),
            TransactionArgument(market_address, Serializer.struct),
            TransactionArgument(market_name, Serializer.str),
            TransactionArgument(creator, Serializer.struct),
            TransactionArgument(collection, Serializer.str),
            TransactionArgument(name, Serializer.str),
            TransactionArgument(property_version, Serializer.u64),
            TransactionArgument(price, Serializer.u64),
        ]

        payload = EntryFunction.natural(
            MKP_ADDRESS,
            "list_token",
            [
                TypeTag(StructTag.from_str("0x1::aptos_coin::AptosCoin"))
            ],
            transaction_arguments
        )
        signed_transaction = self.create_single_signer_bcs_transaction(
            seller, TransactionPayload(payload)
        )

        return self.submit_bcs_transaction(signed_transaction)
