#!/usr/bin/env python3
"""
Basic Flask app with a single GET route that returns a JSON payload.
"""
from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/", methods=["Get"])
def home_app():
    '''Route for the root URL that returns a welcome message in JSON format'''
    return ({"message": "Bienvenue"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")