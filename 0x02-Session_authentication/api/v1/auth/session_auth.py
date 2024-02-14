#!/usr/bin/env python3
"""Session Authentication module"""
from api.v1.auth.auth import Auth
import uuid


class SessionAuth(Auth):
    """Session Authentication class"""

    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Creates a session ID for the user_id"""
        if user_id is None or type(user_id) != str:
            return None
        # generating a session id using uuid
        # and converting it to a string
        # since the method returns a string
        sessionID = str(uuid.uuid4())
        SessionAuth.user_id_by_session_id[sessionID] = user_id
        return sessionID
