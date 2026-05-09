#!/usr/bin/env python3
"""
secure_app.py
─────────────
Secure, refactored version of vulnerable_app.py
All 6 vulnerability classes have been remediated.

CodeAlpha Cybersecurity Internship — Task 3 (Secure Coding Review)
"""

import sqlite3
import subprocess
import os
import re
from flask import Flask, request, escape
from dotenv import load_dotenv  # pip install python-dotenv

load_dotenv()  # Load secrets from .env file — never hardcode

app = Flask(__name__)

# ── FIX 1: Load secrets from environment variables ───────────────
SECRET_KEY = os.getenv("SECRET_KEY")
DB_PASSWORD = os.getenv("DB_PASSWORD")
API_KEY = os.getenv("API_KEY")

# ── FIX 2: Parameterized query — prevents SQL Injection ──────────
@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "").strip()

    if not username or not password:
        return "Missing credentials", 400

    conn = sqlite3.connect("users.db")
    # SAFE: Parameterized query — no string interpolation
    query  = "SELECT * FROM users WHERE username = ? AND password = ?"
    result = conn.execute(query, (username, password)).fetchone()
    conn.close()

    if result:
        return "Login successful"
    return "Invalid credentials", 401

# ── FIX 3: Whitelist validation — prevents Command Injection ─────
HOSTNAME_RE = re.compile(r'^[a-zA-Z0-9.\-]{1,253}$')

@app.route("/ping")
def ping():
    host = request.args.get("host", "")

    # SAFE: Strict whitelist — only valid hostnames allowed
    if not HOSTNAME_RE.match(host):
        return "Invalid hostname", 400

    # SAFE: shell=False + list args — no shell interpretation
    result = subprocess.run(
        ["ping", "-c", "1", host],
        capture_output=True,
        text=True,
        timeout=5,
        shell=False
    )
    return result.stdout

# ── FIX 4: Escape output — prevents XSS ─────────────────────────
@app.route("/greet")
def greet():
    name = request.args.get("name", "")
    # SAFE: Flask's escape() HTML-encodes special chars
    safe_name = escape(name)
    return f"<h1>Hello, {safe_name}!</h1>"

# ── FIX 5: Restrict file access — prevents Path Traversal ────────
ALLOWED_DIR = "/var/app/public_files"

@app.route("/read")
def read_file():
    filename = request.args.get("file", "")

    # SAFE: Resolve to absolute path and check it stays within allowed dir
    requested_path = os.path.realpath(os.path.join(ALLOWED_DIR, filename))

    if not requested_path.startswith(ALLOWED_DIR):
        return "Access denied", 403

    if not os.path.isfile(requested_path):
        return "File not found", 404

    with open(requested_path, "r") as f:
        return f.read()

# ── FIX 6: Disable debug mode in production ──────────────────────
if __name__ == "__main__":
    debug_mode = os.getenv("FLASK_DEBUG", "False").lower() == "true"
    app.run(debug=debug_mode)   # SAFE: controlled via environment variable
