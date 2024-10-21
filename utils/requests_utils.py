import time

from urllib.parse import urlencode

import requests

from fake_useragent import UserAgent
from loguru import logger

import config as cfg

from utils.utils import extract_ip_from_proxy


def create_session(proxy=None, check_proxy=cfg.check_proxy):
    session = requests.Session()
    cfg.default_headers["User-agent"] = UserAgent().random
    session.headers.update(cfg.default_headers)

    if proxy:
        session.proxies = {"http": proxy, "https": proxy}

    if check_proxy and proxy:
        try:
            proxy_ip = extract_ip_from_proxy(proxy)
            actual_ip = session.get("https://api.ipify.org").text
            if actual_ip != proxy_ip:
                raise Exception(
                    f"Error: Proxy IP ({proxy_ip}) does not match actual IP ({actual_ip}). Stopping script."
                )

            else:
                print(f"Proxy check passed: {actual_ip}")
        except requests.RequestException as e:
            raise Exception(f"Error during proxy check: {e}")

    return session


def request_with_retries(
    session, method, url, retries=5, delay=1, response_format="json", **kwargs
):
    method = method.upper()
    for attempt in range(1, retries + 1):
        try:
            logger.info(f"Attempt {attempt} of {retries}")
            response = session.request(method, url, **kwargs)
            response.raise_for_status()
            if response_format == "json":
                return response.json()
            elif response_format == "text":
                return response.text
            else:
                return response.content
        except requests.RequestException as e:
            logger.error(f"Request failed: {e}")
            if attempt == retries:
                logger.critical("Maximum retry attempts reached, giving up.")
                return None
            logger.info(f"Retrying in {delay} seconds...")
            time.sleep(delay)
    return None
