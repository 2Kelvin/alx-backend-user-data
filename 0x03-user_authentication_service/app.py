#!/usr/bin/env python3
"""Basic Flask app Module"""
from flask import Flask, jsonify, request, abort, redirect
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


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout() -> str:
    sessionID = request.cookies.get('session_id')
    theUser = AUTH.get_user_from_session_id(sessionID)
    if theUser is None:
        abort(403)
    AUTH.destroy_session(theUser.id)
    return redirect('/')


@app.route('/profile', strict_slashes=False)
def profile() -> str:
    """Get a user"""
    sessionID = request.cookies.get('session_id')
    theUser = AUTH.get_user_from_session_id(sessionID)
    if theUser is None:
        abort(403)
    return jsonify({'email': theUser.email})


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_password_token() -> str:
    """Get the reset token"""
    email = request.form.get('email')
    try:
        resetToken = AUTH.get_reset_password_token(email)
    except ValueError:
        abort(403)
    return jsonify({"email": email, "reset_token": resetToken})


@app.route('/reset_password', methods=['PUT'], strict_slashes=False)
def update_password() -> str:
    """Update password end-point"""
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_password = request.form.get('new_password')
    try:
        AUTH.update_password(reset_token, new_password)
        return jsonify({"email": email, "message": "Password updated"}), 200
    except ValueError:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
