#!/usr/bin/env python3
"""
Basic Flask app with a single GET route that returns a JSON payload.
"""
from flask import Flask, jsonify, request
from auth import Auth

AUTH = Auth()
app = Flask(__name__)


@app.route("/", methods=["Get"])
def index() -> str:
    '''Route for the root URL that returns a welcome message in JSON format'''
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"])
def users() -> str:
    """Endpoint to register a user."""
    email = request.form.get("email")
    password = request.form.get("password")

    # Register the user if the user does not exits
    try:
        usr = AUTH.register_user(email, password)
        return jsonify({"email": usr.email, "message": "user created"})
    except ValueError as err:
        return jsonify({"message": "email already registered"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
