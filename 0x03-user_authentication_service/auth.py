#!/usr/bin/env python3
"""
This module define a _hash_password method that takes in a password string
arguments and returns bytes.
The returned bytes is a salted hash of the input password, hashed with
bcrypt.hashpw.
"""
import bcrypt
from sqlalchemy.orm.exc import NoResultFound
from db import DB
from user import User


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
