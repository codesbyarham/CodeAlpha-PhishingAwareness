#!/usr/bin/env python3
"""
vulnerable_app.py
─────────────────
Intentionally insecure Flask web app used as the audit target
for CodeAlpha Task 3 (Secure Coding Review).

DO NOT deploy this in production — it contains deliberate vulnerabilities.
"""

import sqlite3
import subprocess
from flask import Flask, request, render_template_string

app = Flask(__name__)

# ── VULNERABILITY 1: Hardcoded credentials ────────────────────────
SECRET_KEY   = "admin123"          # Never hardcode secrets
DB_PASSWORD  = "root"
API_KEY      = "sk-hardcoded-key"

# ── VULNERABILITY 2: SQL Injection ───────────────────────────────
@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    conn = sqlite3.connect("users.db")
    # VULN: User input directly concatenated into SQL query
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    result = conn.execute(query).fetchone()
    conn.close()

    if result:
        return "Login successful"
    return "Invalid credentials"

# ── VULNERABILITY 3: OS Command Injection ────────────────────────
@app.route("/ping")
def ping():
    host = request.args.get("host")
    # VULN: User input passed directly to shell command
    output = subprocess.check_output(f"ping -c 1 {host}", shell=True)
    return output

# ── VULNERABILITY 4: Cross-Site Scripting (XSS) ──────────────────
@app.route("/greet")
def greet():
    name = request.args.get("name", "")
    # VULN: User input rendered directly into HTML without escaping
    html = f"<h1>Hello, {name}!</h1>"
    return render_template_string(html)

# ── VULNERABILITY 5: Insecure File Read (Path Traversal) ─────────
@app.route("/read")
def read_file():
    filename = request.args.get("file")
    # VULN: No validation — attacker can request ../../etc/passwd
    with open(filename, "r") as f:
        return f.read()

# ── VULNERABILITY 6: Debug mode in production ────────────────────
if __name__ == "__main__":
    app.run(debug=True)   # VULN: debug=True exposes interactive debugger
