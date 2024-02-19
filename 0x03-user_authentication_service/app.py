#!/usr/bin/env python3
"""Basic Flask app Module"""
from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def homeRoute():
    """Default route for the app"""
    return jsonify({"message": "Bienvenue"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
