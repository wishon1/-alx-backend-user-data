#!/usr/bin/env python3
"""module containing the class BasicAuth that inherits from Auth"""
from api.v1.auth.auth import Auth


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
