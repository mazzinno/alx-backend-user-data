#!/usr/bin/env python3
"""
A simple Flask app with user authentication
"""
from flask import Flask, jsonify, request, abort, redirect
from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=["GET"], strict_slashes=False)
def index() -> str:
    """GET /
    Return:
        - Home page payload
    """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"], strict_slashes=False)
def users() -> str:
    """POST /users
    Return:
        - Account creation payload
    """
    email, password = request.form.get("email"), request.form.get("password")
    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=["POST"], strict_slashes=False)
def login() -> str:
    """POST /sessions
    Return:
        - Account login payload
    """
    email, password = request.form.get("email"), request.form.get("password")
    if not AUTH.valid_login(email, password):
        abort(401)
    ssn_id = AUTH.create_session(email)
    response = jsonify({"email": email, "message": "logged in"})
    response.set_cookie("ssn_id", ssn_id)
    return response


@app.route("/sessions", methods=["DELETE"], strict_slashes=False)
def logout() -> str:
    """DELETE /sessions
    Return:
        - Redirects to home route
    """
    ssn_id = request.cookies.get("ssn_id")
    user = AUTH.get_user_from_ssn_id(ssn_id)
    if user is None:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect("/")


@app.route("/profile", methods=["GET"], strict_slashes=False)
def profile() -> str:
    """GET /profile
    Return:
        - User profile information
    """
    ssn_id = request.cookies.get("ssn_id")
    user = AUTH.get_user_from_ssn_id(ssn_id)
    if user is None:
        abort(403)
    return jsonify({"email": user.email})


@app.route("/reset_password", methods=["POST"], strict_slashes=False)
def get_reset_password_token() -> str:
    """POST /reset_password
    Return:
        - User password reset payload
    """
    email = request.form.get("email")
    rst_token = None
    try:
        rst_token = AUTH.get_reset_password_token(email)
    except ValueError:
        rst_token = None
    if rst_token is None:
        abort(403)
    return jsonify({"email": email, "rst_token": rst_token})


@app.route("/reset_password", methods=["PUT"], strict_slashes=False)
def update_password() -> str:
    """PUT /reset_password

    Return:
        - User password updated payload
    """
    email = request.form.get("email")
    rst_token = request.form.get("rst_token")
    new_password = request.form.get("new_password")
    is_password_changed = False
    try:
        AUTH.update_password(rst_token, new_password)
        is_password_changed = True
    except ValueError:
        is_password_changed = False
    if not is_password_changed:
        abort(403)
    return jsonify({"email": email, "message": "Password updated"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
