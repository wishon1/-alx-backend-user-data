#!/usr/bin/env python3

"""
Module for password hashing and verification using bcrypt.
"""

import bcrypt


def hash_password(password: str) -> bytes:
    """
    Generates a salted hash of the given password.

    Args:
        password (str): The plain text password to hash.

    Returns:
        bytes: The salted and hashed password as a byte string.
    """
    # Encode the plain text password to bytes
    encoded_pss = password.encode()
    # Generate a salted hash
    hashed_pss = bcrypt.hashpw(encoded_pss, bcrypt.gensalt())

    return hashed_pss


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Verifies that the provided password matches the stored hashed password.

    Args:
        hashed_password (bytes): The hashed password to check against.
        password (str): The plain text password to verify.

    Returns:
        bool: True if the password matches the hash, False otherwise.
    """
    # Encode the plain text password to bytes
    encoded_pss = password.encode()
    # Check the password against the hashed password
    return bcrypt.checkpw(encoded_pss, hashed_password)
