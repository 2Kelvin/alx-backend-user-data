#!/usr/bin/env python3
"""Authorization class module"""
from flask import request
from typing import List, TypeVar
from os import getenv


class Auth():
    """A class template for authentication purposes"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Check if authentication is required"""
        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True
        for eachExcludedPath in excluded_paths:
            if path.rstrip('/') == eachExcludedPath.rstrip('/'):
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """Fetch auth credentials from authorization header"""
        if request is None:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """Current user public class method"""
        return None

    def session_cookie(self, request=None) -> str | None:
        """Returns a cookie value from a request"""
        if request is None:
            return None
        cookieName = getenv('SESSION_NAME')
        cookievalue = request.cookies.get(cookieName)
        return cookievalue
