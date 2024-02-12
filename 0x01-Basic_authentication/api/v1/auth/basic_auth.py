#!/usr/bin/env python3
"""Basic Authentication module"""
from api.v1.auth.auth import Auth
import base64


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
