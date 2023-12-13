from typing import Dict

from ._custom_errors import TokenMissing
from jwt import decode

def token_parser(token:str, keyword:str|None, verify_signature: bool = False) -> Dict | None:
    """
    Method to parse Bearer token
    :param token: token value
    :param keyword: keyword to parse value of (if None - returns whole dict with keys)
    :param verify_signature: verify signature
    :return: dictionary of parsed values
    """

    if not token :
        raise TokenMissing("Missing token","No token value for parsing.")

    token = token.replace("Bearer ", "")

    decoded = decode(
        token.replace("Bearer ", ""),
        algorithms=["HS256"],
        options={"verify_signature": verify_signature},
    )
    if keyword:
        return decoded.get(keyword, None)
    return decoded