
from ._custom_errors import TokenMissing
from jwt import decode

def token_parser(token:str, keyword:str, verify_signature: bool = False) -> str | None:
    """
    Method to parse Bearer token
    :param token: token value
    :param keyword: keyword to parse value of
    :param verify_signature: verify signature
    :return: found value
    """

    token = token.replace("Bearer ", "")

    if not token :
        raise TokenMissing("Missing token","No token value for parsing.")

    decoded = decode(
        token.replace("Bearer ", ""),
        algorithms=["HS256"],
        options={"verify_signature": verify_signature},
    )

    return decoded.get(keyword, None)