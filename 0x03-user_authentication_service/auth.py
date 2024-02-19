#!/usr/bin/env python3
"""Authentication Module"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4


def _hash_password(password: str) -> bytes:
    """Encrypts a user password"""
    encryptedPswd = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    return encryptedPswd


def _generate_uuid() -> str:
    """Generate a random & unique id string"""
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database."""

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Register a user"""
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            return self._db.add_user(email, _hash_password(password))
        raise ValueError(f'User {email} already exists')

    def valid_login(self, email: str, password: str) -> bool:
        """Checking if the credentials are valid"""
        try:
            theUser = self._db.find_user_by(email=email)
            if theUser is not None:
                encodedParamPswd = password.encode('utf-8')
                theUserEncryptedPswd = theUser.hashed_password
                if bcrypt.checkpw(encodedParamPswd, theUserEncryptedPswd):
                    return True
        except NoResultFound:
            return False
        return False

    def create_session(self, email: str) -> str:
        """Create a session and return a session ID"""
        try:
            theUser = self._db.find_user_by(email=email)
        except NoResultFound:
            return None
        if theUser is None:
            return None
        sessionID = _generate_uuid()
        self._db.update_user(theUser.id, session_id=sessionID)
        return sessionID
