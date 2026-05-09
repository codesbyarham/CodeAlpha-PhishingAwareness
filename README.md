# 🔐 CodeAlpha — Secure Coding Review (Task 3)

A full security audit of an intentionally vulnerable Python/Flask application, with a remediated secure version and a detailed report.

## Files
| File | Description |
|------|-------------|
| `vulnerable_app.py` | The target app with 6 deliberate vulnerabilities |
| `secure_app.py` | Fully remediated, secure version |
| `AUDIT_REPORT.md` | Detailed findings with exploits, CWEs, and fixes |

## Vulnerabilities Covered
1. Hardcoded Credentials (CWE-798)
2. SQL Injection (CWE-89)
3. OS Command Injection (CWE-78)
4. Cross-Site Scripting / XSS (CWE-79)
5. Path Traversal (CWE-22)
6. Debug Mode in Production (CWE-94)

## Educational Purpose
This project demonstrates how to identify, understand, and fix the most common web application security vulnerabilities using Python/Flask.

---
**CodeAlpha Cybersecurity Internship**
