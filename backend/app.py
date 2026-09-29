import os
import time
import random
import secrets

from flask import Flask, request, jsonify, session
from flask_cors import CORS
from werkzeug.security import check_password_hash, generate_password_hash


app = Flask(__name__)

app.secret_key = os.environ.get(
    "SECRET_KEY",
    secrets.token_hex(32)
)

app.config.update(
    SESSION_COOKIE_SAMESITE="None",
    SESSION_COOKIE_SECURE=True,
)

CORS(
    app,
    supports_credentials=True,
    origins=[
        "https://rl897240-del.github.io"
    ]
)

USERNAME = os.environ.get(
    "APP_USERNAME",
    "admin"
)

PASSWORD_HASH = os.environ.get(
    "APP_PASSWORD_HASH",
    generate_password_hash("admin")
)


@app.route("/")
def home():
    return "Python backend is running!"


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}

    username = str(data.get("username", ""))
    password = str(data.get("password", ""))

    password_ok = check_password_hash(
        PASSWORD_HASH,
        password
    )

    if username != USERNAME or not password_ok:
        return jsonify({
            "success": False,
            "error": "Nesprávné uživatelské jméno nebo heslo."
        }), 401

    session["logged_in"] = True
    session["username"] = username

    return jsonify({
        "success": True,
        "username": username
    })


@app.route("/logout", methods=["POST"])
def logout():
    session.clear()

    return jsonify({
        "success": True
    })


@app.route("/check-auth", methods=["GET"])
def check_auth():

    if not session.get("logged_in"):
        return jsonify({
            "logged_in": False
        })

    return jsonify({
        "logged_in": True,
        "username": session.get("username")
    })


@app.route("/run", methods=["POST"])
def run():

    if not session.get("logged_in"):
        return jsonify({
            "success": False,
            "error": "Nejsi přihlášen."
        }), 401

    data = request.get_json() or {}

    try:
        score = int(data.get("score", 0))
        time_ms = int(data.get("time", 0))
        name = str(data.get("name", "")).strip()
        count = int(data.get("count", 1))
        activity_id = int(data.get("activityId", 0))
        template_id = int(data.get("templateId", 0))

        if not name:
            raise ValueError("Jméno je povinné.")

        if score < 0:
            raise ValueError("Score nemůže být záporné.")

        if time_ms < 0:
            raise ValueError("Čas nemůže být záporný.")

        if count < 1 or count > 100:
            raise ValueError("Count musí být mezi 1 a 100.")

        if activity_id < 0:
            raise ValueError("Activity ID není platné.")

        if template_id < 0:
            raise ValueError("Template ID není platné.")

    except (ValueError, TypeError) as error:
        return jsonify({
            "success": False,
            "error": str(error)
        }), 400

    # Simulace zpracování
    time.sleep(1)

    results = []

    for n in range(count):

        bot_name = (
            name
            if count == 1
            else f"{name}{random.randint(1, 1000)}"
        )

        results.append({
            "number": n + 1,
            "name": bot_name,
            "score": score,
            "time": time_ms,
            "activityId": activity_id,
            "templateId": template_id
        })

    return jsonify({
        "success": True,
        "status": "done",
        "results": results
    })


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000))
    )
