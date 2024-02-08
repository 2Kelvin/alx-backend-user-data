#!/usr/bin/env python3
'''Encrypting passwords'''
import bcrypt


def hash_password(password: str) -> bytes:
    '''encrypts a string password'''
    encryptedPswd = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    return encryptedPswd


def is_valid(hashed_password: bytes, password: str) -> bool:
    '''checking if the string password matches the encrypted password'''
    return bcrypt.checkpw(password.encode(), hashed_password)
