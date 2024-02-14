#!/usr/bin/env python3
"""Basic Authentication module"""
from api.v1.auth.auth import Auth
import base64
from models.user import User
from typing import TypeVar


class BasicAuth(Auth):
    """Basic authentication class"""

    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """Decoding base64 authorization credentials to a string"""
        if authorization_header is None or type(authorization_header) != str:
            return None
        if authorization_header[:6] != 'Basic ':
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """Decoding a base64 string"""
        if base64_authorization_header is None \
                or type(base64_authorization_header) != str:
            return None
        try:
            return (
                base64.b64decode(base64_authorization_header).decode('utf-8')
            )
        except base64.binascii.Error:
            return None
        except UnicodeDecodeError:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """Get user credentials: email & password from base64 encoded string"""
        if decoded_base64_authorization_header is None or type(
            decoded_base64_authorization_header) != str or \
                ':' not in decoded_base64_authorization_header:
            return (None, None)
        try:
            colonIdx = decoded_base64_authorization_header.index(':')
            userEmail = decoded_base64_authorization_header[:colonIdx]
            userPswd = decoded_base64_authorization_header[(colonIdx + 1):]
            return (userEmail, userPswd)
        except ValueError:
            return (None, None)

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """Returns a user based on their email & password credentials"""
        if user_email is None or type(user_email) != str \
                or user_pwd is None or type(user_pwd) != str:
            return None
        try:
            userList = User.search({'email': user_email})
        except Exception:
            return None
        if len(userList) <= 0:
            return None
        if userList[0].is_valid_password(user_pwd):
            return userList[0]

    def current_user(self, request=None) -> TypeVar('User'):
        """Retrieve a user from a request"""
        authCredentials = self.authorization_header(request)
        encodedAuth = self.extract_base64_authorization_header(authCredentials)
        decodedAuthStr = self.decode_base64_authorization_header(encodedAuth)
        (usrEmail, usrPswd) = self.extract_user_credentials(decodedAuthStr)
        user = self.user_object_from_credentials(usrEmail, usrPswd)
        return user
