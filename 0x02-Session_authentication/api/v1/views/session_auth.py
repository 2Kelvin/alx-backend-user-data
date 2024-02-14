#!/usr/bin/env python3
"""Session Routes Module"""

from typing import Tuple
from api.v1.views import app_views
from flask import request, jsonify, abort
from models.user import User
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def authenticateSessions() -> Tuple[str, int]:
    """Handles all routes for session authentication"""
    usrEmail = request.form.get('email')
    usrPassword = request.form.get('password')
    if usrEmail is None or len(usrEmail.strip()) == 0:
        return jsonify({"error": "email missing"}), 400
    if usrPassword is None or len(usrPassword.strip()) == 0:
        return jsonify({"error": "password missing"}), 400
    try:
        users = User.search({'email': usrEmail})
    except Exception:
        return jsonify({"error": "no user found for this email"}), 404
    if len(users) <= 0:
        return jsonify({"error": "no user found for this email"}), 404
    if users[0].is_valid_password(usrPassword):
        from api.v1.app import auth
        sessionID = auth.create_session(getattr(users[0], 'id'))
        data = jsonify(users[0].to_json())
        data.set_cookie(getenv('SESSION_NAME'), sessionID)
        return data
    return jsonify({"error": "wrong password"}), 401


@app_views.route(
    '/auth_session/logout', methods=['DELETE'], strict_slashes=False)
def logoutFromSession() -> Tuple[str, int]:
    """Logout session route"""
    from api.v1.app import auth
    toBeDestroyed = auth.destroy_session(request)
    if not toBeDestroyed:
        abort(404)
    return jsonify({})
