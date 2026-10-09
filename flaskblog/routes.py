from flask import request, jsonify, render_template, flash, redirect, url_for
from flaskblog import app
from flaskblog.models import User, AuthService
import logging

# Log errors internally without crashing the app
logging.basicConfig(level=logging.ERROR, filename="app_errors.log")

# Instantiate OOP Service
auth_service = AuthService()

@app.route("/login", methods=['POST'])
def login():
    # A. PARSE INPUT SAFELY
    if not request.is_json:
        return jsonify({"success": False, "message": "Expected JSON payload"}), 400

    data = request.get_json(silent=True)
    if data is None:
        return jsonify({"success": False, "message": "Malformed JSON payload"}), 400

    email = data.get("email")
    password = data.get("password")

    # B. DELEGATE AUTHENTICATION & VALIDATION TO AUTH SERVICE
    result, status_code = auth_service.authenticate_user(email, password)

    # C. RESOLVE REDIRECT URL IF SUCCESSFUL
    if result.get("success") and result.get("redirect_url") == "home":
        result["redirect_url"] = url_for("home")

    return jsonify(result), status_code