#!/usr/bin/env python3
"""
This module define a _hash_password method that takes in a password string
arguments and returns bytes.
The returned bytes is a salted hash of the input password, hashed with
bcrypt.hashpw.
"""
import bcrypt


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
