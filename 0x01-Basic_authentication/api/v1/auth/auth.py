#!/usr/bin/env python3
"""module to manage the the API authentication."""
from flask import request
from typing import List, TypeVar


class Auth:
    """class to manage the API authentication"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Define which routes don't need authentication"""
        if path is None:
            return True

        if excluded_paths is None or not excluded_paths:
            return True

        # Nomalize path by ensuring it ends with a slash
        if not path.endswith('/'):
            path += '/'

        for excluded_path in excluded_paths:
            # Normalize excluded_path by ensuring it ends with a slash
            if not excluded_path.endswith('/'):
                excluded_path += '/'

            if path == excluded_path:
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """returns None - request will be the Flask request object"""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """returns None - request will be the Flask request object"""
        return None
