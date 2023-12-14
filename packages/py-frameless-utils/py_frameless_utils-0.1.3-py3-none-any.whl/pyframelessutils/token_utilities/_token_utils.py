"""
Module containing functionality related with tokens
"""
from jwt import decode

from .exceptions import TokenUtilitiesException


def token_parser(
    token: str,
    keyword: str = None,
    algorithm_list: list = None,
    verify_signature: bool = False,
    decode_key: str = None,
) -> str | dict | None:
    """
    Method to parse Bearer token
    :param token: token value
    :param keyword: keyword to parse value of (if None - returns whole dict with keys)
    :param algorithm_list: list with algorithms. Default HS256
    :param verify_signature: verify signature
    :param decode_key: key for signature verification
    :return: value by keyword, dictionary or None
    """

    if not token:
        raise TokenUtilitiesException("Missing token", "No token value for parsing.")
    token = token.replace("Bearer ", "")

    if not algorithm_list:
        algorithm_list = ["HS256"]

    if verify_signature and not decode_key:
        raise TokenUtilitiesException(
            "Missing secret", "Secret key was not provided for verification"
        )

    decoded = decode(
        token.replace("Bearer ", ""),
        algorithms=algorithm_list,
        key=decode_key,
        options={"verify_signature": verify_signature},
    )
    return decoded.get(keyword) if keyword else decoded
