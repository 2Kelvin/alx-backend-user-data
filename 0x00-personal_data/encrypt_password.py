#!/usr/bin/env python3
'''Encrypting passwords'''
import bcrypt
from typing import ByteString


def hash_password(password: str) -> ByteString:
    '''encrypts a string password'''
    encryptedPswd = bcrypt.hashpw(bytes(password), bcrypt.gensalt())
    return encryptedPswd
