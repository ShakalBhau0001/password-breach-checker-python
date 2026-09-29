import hashlib

import requests

API_URL = "https://api.pwnedpasswords.com/range/"


def check_password(password: str) -> int:
    sha1 = hashlib.sha1(password.encode("utf-8")).hexdigest().upper()
    prefix, suffix = sha1[:5], sha1[5:]
    response = requests.get(API_URL + prefix, timeout=10)
    if response.status_code != 200:
        raise RuntimeError(f"API request failed: {response.status_code}")

    for line in response.text.splitlines():
        hash_suffix, count = line.split(":")
        if hash_suffix == suffix:
            return int(count)

    return 0


def check_multiple(passwords: list[str]) -> dict[str, int]:
    return {pw: check_password(pw) for pw in passwords}


def mask_password(password: str) -> str:
    if len(password) <= 2:
        return "*" * len(password)
    return password[:2] + "*" * (len(password) - 2)
