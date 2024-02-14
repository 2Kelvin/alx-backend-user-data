#!/usr/bin/env python3
"""Session Authentication module"""
from api.v1.auth.auth import Auth
import uuid
from models.user import User


class SessionAuth(Auth):
    """Session Authentication class"""

    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Creates a session ID for the user_id"""
        if user_id is None or type(user_id) != str:
            return None
        # generating a session id using uuid
        # and converting it to a string
        # since the method returns a sessionID string
        sessionID = str(uuid.uuid4())
        SessionAuth.user_id_by_session_id[sessionID] = user_id
        return sessionID

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Returns a user_id based on their sessionID"""
        if session_id is None or type(session_id) != str:
            return None
        return SessionAuth.user_id_by_session_id.get(session_id)

    def current_user(self, request=None) -> User:
        """Returns a User based on the cookie value"""
        # getting the cookie value
        cookieValue = self.session_cookie(request)
        # using the cookie value as sessionID to fetch user_id
        userID = self.user_id_for_session_id(cookieValue)
        # fetching the user (obj)
        return User.get(userID)

    def destroy_session(self, request=None) -> bool:
        """Deletes a user session on logout"""
        if request is None:
            return False
        sessionID = self.session_cookie(request)
        userID = self.user_id_for_session_id(sessionID)
        if sessionID is None or userID is None:
            return False
        if sessionID in self.user_id_by_session_id:
            del self.user_id_by_session_id[sessionID]
        return True
