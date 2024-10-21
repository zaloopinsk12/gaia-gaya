import time
import random
import json
import math
from datetime import datetime, timedelta
import config as cfg


def current_time():
    cur_time = time.strftime("%Y-%m-%d %H:%M:%S")[:-3]
    return cur_time


def add_access_token_to_file(
    private_key, proxy, user_agent, path="./data/accounts.txt"
):
    valid_until = datetime.now() + timedelta(days=6)
    valid_until_str = valid_until.strftime("%Y-%m-%d")

    # Prepare new account data
    new_account_data = {
        "private_key": private_key,
        "valid_until": valid_until_str,
        "proxies": proxy,
        "user_agent": user_agent,
    }

    # Try to open and read existing file data, append new data in JSON Lines format
    try:
        with open(path, "a") as file:
            # Directly append the new account as a new line in JSON format
            json.dump(new_account_data, file)
            file.write("\n")  # Ensuring each entry is on a new line
    except IOError as e:
        print(f"An error occurred while writing to the file: {e}")


def extract_ip_from_proxy(proxy):
    if proxy.startswith("http://"):
        proxy = proxy[7:]
    elif proxy.startswith("https://"):
        proxy = proxy[8:]

    at_split = proxy.split("@")[-1]
    ip = at_split.split(":")[0]

    return ip


def load_keys_with_proxies():
    private_keys = []
    proxies = []

    with open("./data/keys.txt", "r") as f:
        for line in f:
            line = line.strip()
            private_keys.append(line)

    with open("./data/proxies.txt", "r") as p:
        for proxy in p:
            proxy = proxy.strip()
            proxies.append(proxy)


    return private_keys, proxies


def return_accounts_array(path=cfg.accounts_path):
    with open(path, "r") as file:
        accounts_data = file.readlines()
    return accounts_data
