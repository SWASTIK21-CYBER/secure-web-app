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
```

---

## 🚀 Getting Started

### Prerequisites
* Python 3.8+ installed on your system.

### 1. Installation & Environment Setup

Clone the repository and checkout the `flask-backend` branch:

```bash
git clone https://github.com/YOUR_USERNAME/secure-web-app.git
cd secure-web-app
git checkout flask-backend
```

Create and activate a virtual environment:

* **Windows (CMD):**
  ```cmd
  python -m venv venv
  venv\Scripts\activate
  ```
* **macOS / Linux:**
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

Install required dependencies:

```bash
pip install -r requirements.txt
```

### 2. Environment Configuration

Create a `.env` file in the root directory:

```env
JWT_SECRET=super_secret_key_that_is_at_least_32_bytes_long_123456
```

---

## 🏃 Running the Application

Start the Flask development server:

```bash
python app.py
```

The API will run locally at `http://127.0.0.1:5000`.

---

## 📡 API Endpoints Summary

| Method | Endpoint | Access Level | Description |
| :--- | :--- | :--- | :--- |
| `GET` | `/` | Public | API health check status |
| `POST` | `/register` | Public | Register a new user (`username`, `password`, `role`) |
| `POST` | `/login` | Public (Rate Limited) | Authenticate user & receive JWT token |
| `GET` | `/profile` | Authenticated | Fetch current user profile (Requires `Bearer <token>`) |
| `GET` | `/admin` | Admin Only | Access restricted admin dashboard |

---

## 🧪 Testing the API

An automated test script `test_api.py` is included to verify the registration, login, and token authorization pipeline.

While `app.py` is running in one terminal, open a second terminal and execute:

```bash
python test_api.py
```

**Expected Output:**
```text
✓ Login successful. Token received.
Profile Response: {
  "message": "Access granted to protected route",
  "user": {
    "id": "1",
    "role": "user",
    "username": "testuser"
  }
}
```
