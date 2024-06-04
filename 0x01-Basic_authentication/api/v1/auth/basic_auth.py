#!/usr/bin/env python3
"""module containing the class BasicAuth that inherits from Auth"""
from api.v1.auth.auth import Auth
import base64


class BasicAuth(Auth):
    """Class for Basic Authentication methods"""

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """
        Extracts the Base64 part of the Authorization header for Basic
        Authentication

        Args:
            authorization_header (str): The authorization header to extract the
            Base64 part from

        Returns:
            str: The Base64 part of the header if present, otherwise None
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None

        return authorization_header[len("Basic "):]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header:
                                           str) -> str:
        """
        Decodes the Base64 part of the Authorization header for Basic
        Authentication

        Args:
            base64_authorization_header (str): The Base64 string to decode

        Returns:
            str: The decoded value as a UTF-8 string if successful,
            otherwise None
        """
        if base64_authorization_header is None:
            return None
        if type(base64_authorization_header) is not str:
            return None

        try:
            decoded_bytes = base64.b64decode(base64_authorization_header)
            return decoded_bytes.decode('utf-8')
        except (base64.binascii.Error, UnicodeDecodeError):
            return None

    def extract_user_credentials(self, decoded_base64_authorization_header:
                                 str) -> (str, str):
        """
        method that returns returns the user email and password from the Base64
        decoded value.

        Args:
            decoded_base64_authorization_heade (str): Base64 decoded string

            Returns:
                 tuple: user email and password or (None, None) if invalid
                 input
        """
        if decoded_base64_authorization_header is None:
            return (None, None)
        if not isinstance(decoded_base64_authorization_header, str):
            return (None, None)
        if ':' not in decoded_base64_authorization_header:
            return (None, None)

        usr_email, usr_password = \
            decoded_base64_authorization_header.split(':', 1)
        return usr_email, usr_password
