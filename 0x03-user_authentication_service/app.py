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


@app.route("/sessions", methods=["DELETE"])
def logout():
    """
    Logs out a user by destroying their session.

    Expects a session ID in the request cookies with the key
    "session_id". If the session ID is valid, destroys the session and
    redirects to the home page. If not, returns a 403 HTTP status.
    """

    # Extract the session ID from the request cookies
    session_id = request.cookies.get("session_id")

    # Get the user associated with the session ID
    user = AUTH.get_user_from_session_id(session_id)

    # If no user is found, abort with a 403 HTTP status
    if not user:
        abort(403)

    # Destroy the session for the user
    AUTH.destroy_session(user.id)

    # Redirect the user to the home page
    return redirect('/')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
