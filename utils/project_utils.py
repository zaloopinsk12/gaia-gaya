import json
import random
import re
import string
import time

from fake_useragent import UserAgent
from loguru import logger
from web3 import Web3

import config as cfg

from utils.requests_utils import create_session, request_with_retries
from utils.utils import add_access_token_to_file, return_accounts_array
from utils.web3_utils import initialize_account, sign_with_key, create_web3_with_proxy

def create_acc_vars(private_key, proxy, RPC):
    account = initialize_account(private_key)
    web3 = create_web3_with_proxy(RPC, proxy)
    session = create_session(proxy)

    return account, web3, session


def setup_account(account_dict, rpc=None):
    return create_acc_vars(account_dict["private_key"], account_dict["proxies"], rpc)


def create_acc_dicts(
    private_key, proxy, save=True
):  # creates account dict in accounts.txt {private_key, proxy, user_agent}. access_token etc can also be added
    account, web3, session = create_acc_vars(private_key, proxy, None)
    user_agent = session.headers["User-Agent"]
    if save == True:
        acc_dict = add_access_token_to_file(
            private_key=private_key,
            proxy=proxy,
            user_agent=user_agent,
            path="./data/accounts.txt",
        )
    logger.info(f"{account.address} | Created account dict for work ")

    return acc_dict


def get_signature(account):
    current_timestamp = int(time.time())
    message_dict = {
        "wallet_address": account.address,
        "timestamp": current_timestamp
    }
    
    message = json.dumps(message_dict, separators=(',', ':'))
    signature = sign_with_key(message, account.key)
    print(message)
    return signature, current_timestamp


def get_user_id(account_dict):
    account = initialize_account(account_dict["private_key"])
    signature, timestamp = get_signature(account)
    session = create_session(account_dict["proxies"])
    json_data = {
        'signature': signature,
        'message': {
            'wallet_address': account.address,
            'timestamp': timestamp,
        },
    }

    response = session.post('https://api.gaianet.ai/api/v1/users/connect-wallet/', json=json_data)
    user_id = response.json()["data"]["user_id"]
    if user_id:
        logger.success(f"Got user ID: {user_id}")

    return user_id, session


def train_model(account_dict):
    session = create_session(account_dict["proxies"])
    user_id, session = get_user_id(account_dict)

    with open('./data/content.txt', 'r') as f:
        phrases = [line.strip() for line in f if line.strip()]

    n_messages = random.randint(cfg.messages_per_chat[0], cfg.messages_per_chat[1])

    messages = [
        {
            "role": "system",
            "content": cfg.system_prompt
        }
    ]

    for _ in range(n_messages):
        user_phrase = random.choice(phrases)

        messages.append({
            "role": "user",
            "content": user_phrase
        })

        json_data = {
            "model": "Qwen1.5-0.5B-Chat-Q5_K_M",
            "messages": messages,
            "stream": True,
            "stream_options": {
                "include_usage": True
            },
            "user": user_id
        }

        response = session.post(
            'https://qwencoder.us.gaianet.network/v1/chat/completions',
            json=json_data,
        )

        full_content = ''

        for line in response.iter_lines():
            if line:
                decoded_line = line.decode('utf-8')
                if decoded_line.startswith('data: '):
                    json_data_line = decoded_line[len('data: '):]
                    if json_data_line.strip() == '[DONE]':
                        continue
                    try:
                        data = json.loads(json_data_line)
                        choices = data.get('choices', [])
                        if not choices:
                            continue
                        delta = choices[0].get('delta', {})
                        content = delta.get('content', '')
                        full_content += content
                    except json.JSONDecodeError as e:
                        print(f"JSON decode error: {e}")
                        continue
                    except IndexError as e:
                        print(f"Index error: {e}")
                        continue
                    except KeyError as e:
                        print(f"Key error: {e}")
                        continue

        messages.append({
            "role": "assistant",
            "content": full_content
        })

        print(full_content)
        sleep_time = random.randint(*cfg.sleep_between)
        print(f"Sleeping for {sleep_time} seconds")
        time.sleep(sleep_time)
