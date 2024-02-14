#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os
from api.v1.auth.auth import Auth
from api.v1.auth.basic_auth import BasicAuth
from api.v1.auth.session_auth import SessionAuth


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
auth = None
authType = getenv('AUTH_TYPE')

if authType == 'basic_auth':
    auth = BasicAuth()
elif authType == 'session_auth':
    auth = SessionAuth()
else:
    auth = Auth()


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorizedRequest(error) -> str:
    """Handling unauthorized request error"""
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbiddenRequest(error) -> str:
    """Handling forbidden access request error"""
    return jsonify({"error": "Forbidden"}), 403


@app.before_request
def filter():
    """Filtering each request"""
    pathList = ['/api/v1/status/', '/api/v1/unauthorized/',
                '/api/v1/forbidden/', '/api/v1/auth_session/login/']
    if auth is None:
        return
    elif not auth.require_auth(path=request.path, excluded_paths=pathList):
        return
    elif auth.authorization_header(request) is None \
            and auth.session_cookie(request) is None:
        abort(401)
    elif auth.current_user(request) is None:
        abort(403)
    else:
        authorization = auth.authorization_header(request)
        request.current_user = auth.current_user(request)


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
