#!/usr/bin/env python3
"""
module for authenticsting the session
"""
from .auth import Auth
from models.user import User
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

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        returns a User ID based on a Session ID

        Args:
            session_id (str): the session id which is a string

        Return: Return None if session_id is None or session_id is not a string
        """
        if not isinstance(session_id, str) or session_id is None:
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """
        overload) that returns a User instance based on a cookie value
        """
        session_cookie = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_cookie)
        return User.get(user_id)
