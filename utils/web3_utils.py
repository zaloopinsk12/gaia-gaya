import time
import random

from requests.sessions import Session

from eth_abi import abi, encode
from eth_account.messages import encode_defunct

from web3 import Web3
from web3.middleware import geth_poa_middleware
from web3.providers.rpc import HTTPProvider
from web3.exceptions import ContractLogicError

from loguru import logger

from utils import utils
import config as cfg


def create_web3_with_proxy(rpc_endpoint, proxy=None):
    if proxy is None:
        return Web3(Web3.HTTPProvider(rpc_endpoint))

    proxy_settings = {
        "http": proxy,
        "https": proxy,
    }

    session = Session()
    session.proxies = proxy_settings

    custom_provider = HTTPProvider(rpc_endpoint, session=session)
    web3 = Web3(custom_provider)
    web3.middleware_onion.inject(geth_poa_middleware, layer=0)

    return web3


def initialize_account(private_key):
    web3 = Web3()

    return web3.eth.account.from_key(private_key)


def sign_with_key(message_to_sign, private_key):  # returns signature
    account = initialize_account(private_key)
    signature = account.sign_message(
        encode_defunct(text=message_to_sign)
    ).signature.hex()

    return signature
