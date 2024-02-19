#!/usr/bin/env python3
"""Authentication Module"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """Encrypts a user password"""
    encryptedPswd = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    return encryptedPswd
