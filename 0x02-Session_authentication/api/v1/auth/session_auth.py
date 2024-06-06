#!/usr/bin/env python3
"""
module for authenticsting the session
"""
from .auth import Auth
import uuid


class SessionAuth(Auth):
    """SessionAuth that inherits from Auth"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        creates a Session ID for a user_id

        Args:
            user_id (strt): the user id
            Returns:
                Return None if user_id is None or if user_id is not a string
        """
        if not isinstance(user_id, str) or user_id is None:
            return None
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id
