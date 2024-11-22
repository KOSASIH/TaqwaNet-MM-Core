# src/blockchain/utils.py

from web3 import Web3
import json
import logging

def get_contract_instance(web3, contract_address, abi_path):
    """Get a contract instance."""
    with open(abi_path) as abi_file:
        abi = json.load(abi_file)
    return web3.eth.contract(address=contract_address, abi=abi)

def sign_transaction(transaction, private_key):
    """Sign a transaction with the provided private key."""
    web3 = Web3()
    signed_txn = web3.eth.account.signTransaction(transaction, private_key)
    return signed_txn

def decode_event(event):
    """Decode an event log."""
    return {
        'event': event['event'],
        'args': event['args'],
        'blockNumber': event['blockNumber'],
        'transactionHash': event['transactionHash'].hex(),
    }

def wait_for_transaction_receipt(web3, txn_hash, timeout=120):
    """Wait for a transaction receipt."""
    import time
    start_time = time.time()
    while True:
        receipt = web3.eth.getTransactionReceipt(txn_hash)
        if receipt is not None:
            return receipt
        if time.time() - start_time > timeout:
            raise Exception("Transaction receipt not found within timeout period.")
        time.sleep(1)
