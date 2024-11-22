# src/blockchain/blockchain_service.py

from web3 import Web3
from web3.exceptions import TransactionNotFound
import json
import logging
from .utils import get_contract_instance, sign_transaction

class BlockchainService:
    def __init__(self, provider_url, private_key, contract_address, abi_path):
        self.web3 = Web3(Web3.HTTPProvider(provider_url))
        self.private_key = private_key
        self.contract_address = contract_address
        self.contract = get_contract_instance(self.web3, contract_address, abi_path)
        self.logger = logging.getLogger(__name__)

    def is_connected(self):
        """Check if the connection to the blockchain is successful."""
        return self.web3.isConnected()

    def send_transaction(self, function_name, *args):
        """Send a transaction to the blockchain."""
        if not self.is_connected():
            self.logger.error("Blockchain connection failed.")
            return None

        nonce = self.web3.eth.getTransactionCount(self.web3.eth.defaultAccount)
        transaction = self.contract.functions[function_name](*args).buildTransaction({
            'chainId': 1,  # Mainnet
            'gas': 2000000,
            'gasPrice': self.web3.toWei('50', 'gwei'),
            'nonce': nonce,
        })

        signed_txn = sign_transaction(transaction, self.private_key)
        txn_hash = self.web3.eth.sendRawTransaction(signed_txn.rawTransaction)
        self.logger.info(f"Transaction sent: {txn_hash.hex()}")
        return txn_hash.hex()

    def get_transaction_receipt(self, txn_hash):
        """Get the transaction receipt."""
        try:
            receipt = self.web3.eth.getTransactionReceipt(txn_hash)
            if receipt is None:
                self.logger.warning("Transaction not found.")
                return None
            return receipt
        except TransactionNotFound:
            self.logger.error("Transaction not found.")
            return None

    def call_contract_function(self, function_name, *args):
        """Call a smart contract function without sending a transaction."""
        if not self.is_connected():
            self.logger.error("Blockchain connection failed.")
            return None

        result = self.contract.functions[function_name](*args).call()
        self.logger.info(f"Function {function_name} called with result: {result}")
        return result
