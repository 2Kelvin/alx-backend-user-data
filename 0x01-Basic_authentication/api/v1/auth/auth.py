#!/usr/bin/env python3
"""Auth class module"""
from flask import request
from typing import List, TypeVar


class Auth():
    """A class template for authentication purposes"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Check if authentication is required"""
        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True
        for eachExcludedPath in excluded_paths:
            if path.removesuffix('/') == eachExcludedPath.removesuffix('/'):
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """Authorization header method"""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Current user public class method"""
        return None
