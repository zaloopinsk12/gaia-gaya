import time
import json
from sys import stderr
from concurrent.futures import ThreadPoolExecutor, as_completed

from loguru import logger

from utils.web3_utils import initialize_account
import utils.project_utils as prj
from utils.utils import return_accounts_array, load_keys_with_proxies

import config as cfg

# Setup logging
logger.remove()
logger.add(
    stderr,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{function}</cyan> | <level>{message}</level> | <yellow>{thread}</yellow>",
)


def worker(func, account_info):
    try:
        account_dict = json.loads(account_info)
        func(account_dict)  # Process the account with the provided function
    except Exception as e:
        account_address = "Unknown"
        try:
            if "private_key" in account_dict:
                account_address = initialize_account(
                    account_dict["private_key"]
                ).address
        except Exception:
            pass

        error_message = f"Error for address: {account_address} | Error: {e}"
        logger.error(error_message)

        with open("./data/fail_logs.txt", "a") as log_file:
            log_file.write(error_message + "\n")


def process_accounts(func, workers=cfg.workers):
    accounts_array = return_accounts_array()
    with ThreadPoolExecutor(max_workers=workers) as executor:
        future_to_account = {
            executor.submit(worker, func, account_info): account_info
            for account_info in accounts_array
        }

        for future in as_completed(future_to_account):
            account_info = future_to_account[future]
            try:
                future.result()  # Re-raises any exceptions caught in the worker
            except Exception as exc:
                logger.error(
                    f"Account processing failed for {account_info}: {exc}")


if __name__ == "__main__":
    choice = int(
        input(
            "\n----------------------"
            "\n1: Create accounts{} for work (accounts.txt)"
            "\n2 Start training model"
            "\nChoice: "
        )
    )

    transaction_functions = {
        1: lambda: [
            prj.create_acc_dicts(key, proxy, save=True)
            for key, proxy in zip(*load_keys_with_proxies())
        ],
        2: lambda: process_accounts(prj.train_model),
    }

    if choice in transaction_functions:
        transaction_functions[choice]()
    else:
        print("Wrong choice number. 1 | 2 | 3 ...")
