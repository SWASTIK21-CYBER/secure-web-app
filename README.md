# Secure Web Application API (Flask & JWT)

A security-focused RESTful API built with Python and Flask, engineered according to **OWASP security best practices**. This project demonstrates robust Role-Based Access Control (RBAC), secure authentication using JSON Web Tokens (JWT), salted password hashing, rate limiting, and protection against common web vulnerabilities.

> **Branch Architecture Notice:**
> * `main` branch: Original Node.js / Express backend implementation.
> * `flask-backend` branch (Current): Complete 100% Python / Flask implementation.

---

## 🛠️ Tech Stack

* **Backend Framework:** Python / Flask
* **Database:** SQLite3
* **Authentication:** PyJWT (JSON Web Tokens)
* **Password Hashing:** Bcrypt (Salted blowfish hashing)
* **Rate Limiting:** Flask-Limiter
* **Environment Management:** python-dotenv

---

## 🔒 Security & OWASP Implementation

This API implements key controls addressing the **OWASP Top 10** web application security risks:

1. **SQL Injection Prevention (OWASP A03:2021):**
   * All database operations utilize **parameterized SQL queries** (`?` placeholders) to prevent SQL injection attacks.

2. **Broken Access Control & Authentication (OWASP A01:2021 & A07:2021):**
   * **JWT Validation:** Custom `@token_required` decorator validates signature, expiration (`exp`), and token integrity.
   * **Role-Based Access Control (RBAC):** Custom `@role_required("admin")` decorator enforces granular route-level permissions.
   * **Cryptographic Keys:** Utilizes high-entropy keys (32+ bytes) with HMAC-SHA256 signing.

3. **Identification & Authentication Failures (OWASP A07:2021):**
   * **Bcrypt Hashing:** Passwords are never stored in plaintext. They are salted and hashed using `bcrypt.hashpw()` before database insertion.

4. **Identification & Brute-Force Defense:**
   * **Rate Limiting:** Enforced via `Flask-Limiter` (`5 requests/min` on `/login`) to stop automated credential stuffing and brute-force attacks.

---

## 📁 Repository Structure

```text
secure-web-app/
│
├── app.py              # Main Flask application logic, database setup & security middleware
├── test_api.py         # Automated integration test script for authentication flow
├── requirements.txt    # Project dependencies
├── .env.example        # Template for environment variables
├── .gitignore          # Rules for ignoring venv, databases, and secrets
└── README.md           # Project documentation
