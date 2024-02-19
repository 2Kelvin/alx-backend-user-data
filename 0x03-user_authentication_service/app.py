#!/usr/bin/env python3
"""Basic Flask app Module"""
from flask import Flask, jsonify, request, abort
from auth import Auth

AUTH = Auth()

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def homeRoute() -> str:
    """Default route for the app"""
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def users() -> str:
    """Endpoint to register users"""
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        AUTH.register_user(email=email, password=password)
        return jsonify({
            'email': email,
            'message': 'user created'
        })
    except ValueError:
        return jsonify({'message': 'email already registered'}), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login() -> str:
    """Login with credentials"""
    email = request.form.get('email')
    password = request.form.get('password')
    if not AUTH.valid_login(email, password):
        abort(401)
    sessionID = AUTH.create_session(email)
    output = jsonify({"email": email, "message": "logged in"})
    output.set_cookie('session_id', sessionID)
    return output


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
