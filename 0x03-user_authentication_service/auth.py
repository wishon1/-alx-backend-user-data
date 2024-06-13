#!/usr/bin/env python3
"""
This module define a _hash_password method that takes in a password string
arguments and returns bytes.
The returned bytes is a salted hash of the input password, hashed with
bcrypt.hashpw.
"""
import bcrypt
import uuid

from sqlalchemy.orm.exc import NoResultFound
from db import DB
from user import User
from typing import Union


def _hash_password(password: str) -> bytes:
    """
    Hashes a password using bcrypt.

    Args:
        password (str): The password to hash.

    Returns:
        bytes: The salted hash of the password.
    """
    # generate the salted hash
    salt_hash = bcrypt.gensalt()

    # hash the password with the generated salt
    hashed_pw = bcrypt.hashpw(password.encode(), salt_hash)

    return hashed_pw


def _generate_uuid() -> str:
    """
    Generate a new UUID.

    This function generates and returns a string representation of a
    new UUID. It is a private method and should not be used outside of
    the auth module.

    Returns:
        str: The string representation of the generated UUID.
    """
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Register a new user withh the given email and password.

        Args:
            email (str): The email of the user to register.
            password (str): The password of the user to register

        Returns:
            ValueError: if a user with the given email already exists
        """
        # check if the user with the given email already exists
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            pass

        # Hash the password
        hashed_pwd = _hash_password(password)

        # Add the new user to the database
        usr = self._db.add_user(email=email, hashed_password=hashed_pwd)
        return usr

    def valid_login(self, email: str, password: str) -> bool:
        """
        Validates user login credentials.

        This method checks if the provided email and password combination
        is correct by fetching the user from the database using the email
        and then verifying the password using bcrypt.

        Args:
            email (str): The user's email address.
            password (str): The user's plaintext password.

        Returns:
            bool: True if the email and password are valid, False otherwise.
        """
        try:
            # Attempt to retrieve the user from the database by email
            usr = self._db.find_user_by(email=email)
        except NoResultFound:
            # Return False if no user is found with the provided email
            return False

        # Verify the provided password against the stored hashed password
        return bcrypt.checkpw(password.encode('utf-8'), usr.hashed_password)

    def create_session(self, email: str) -> str:
        """
        Find the user corresponding to the email, generate a new UUID and
        store it in the database as the user's session_id, then return the
        session ID.

        Args:
            email (str): The user's email address.

        Returns:
            str: The session ID as a string.

        Raises:
            ValueError: If the user is not found.
        """
        # Attempt to retrieve the user from the database using the provided
        # email
        try:
            usr = self._db.find_user_by(email=email)
        except NoResultFound:
            # If no user is found with the provided email, return None
            usr = None

        # Raise a ValueError if the user is not found
        if usr is None:
            return None

        # Generate a new UUID to be used as the session ID
        session_id = _generate_uuid()

        # Update the user's session_id in the database
        self._db.update_user(usr.id, session_id=session_id)

        # Return the newly generated session ID
        return session_id

    def get_user_from_session_id(self, session_id:
                                 str) -> Union[User, None]:
        """
        Retrieve a user based on the session ID.

        Args:
            session_id (str): The session ID associated with
            the user session.

        Returns:
            User or None: The User object if a corresponding
            user is found; otherwise, None.
        """
        if not session_id:
            return None

        try:
            # Try to find the user by the session_id using the database
            # public method
            usr = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            # If no user is found, return None
            return None

        return usr

    def destroy_session(self, user_id: int) -> None:
        """update the corresponding user id to None"""
        if not user_id:
            return
        try:
            usr = self._db.find_user_by(id=user_id)
            self.db.update_user(usr.id, session_id=None)
        except Exception:
            pass
