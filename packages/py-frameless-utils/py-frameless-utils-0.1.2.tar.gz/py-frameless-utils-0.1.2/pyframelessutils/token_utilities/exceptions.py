"""
Module to define custom exceptions.

"""
from typing import Any


class TokenUtilitiesException(Exception):
    """
    Class for missing token exception
    """

    def __init__(self, message: str = None, detail: Any = None):
        """
        Constructor
        :param message: message to return
        :param detail: detail information to return
        """
        self.message = message
        self.detail = detail
