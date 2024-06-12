#!/usr/bin/env python3
"""
Basic Flask app with a single GET route that returns a JSON payload.
"""
from flask import Flask, jsonify, request, abort
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


@app.route("/sessions", methods=["POST"])
def login() -> str:
    """
    Handle user login by validating email and password, creating
    a session, and responding with a session ID cookie if successful.

    Returns:
        str: A JSON response containing the user's email and a success
        message if the login is successful. If the login fails, aborts with
        a 401 status.
    """
    # Retrieve email and password from the form data in the request
    email = request.form.get("email")
    password = request.form.get("password")

    # Validate the login credentials
    if AUTH.valid_login(email, password):
        # Create a new session for the user
        session_id = AUTH.create_session(email)

        # Create a JSON response with the user's email and a success message
        response = jsonify({"email": email, "message": "logged in"})

        # Set a cookie on the response with the session ID
        response.set_cookie("session_id", session_id)

        return response
    else:
        # Abort with a 401 Unauthorized status if login is invalid
        abort(401)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
