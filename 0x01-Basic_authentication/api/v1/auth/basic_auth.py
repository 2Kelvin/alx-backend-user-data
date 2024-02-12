#!/usr/bin/env python3
"""Basic Authentication module"""
from api.v1.auth.auth import Auth


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
