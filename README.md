# Secure Task Management Web Application

A lightweight, security-hardened RESTful API built with **Node.js**, **Express**, and **SQLite**. This application demonstrates core web application security concepts, implementing robust mechanisms for authentication, role-based access control (RBAC), rate limiting, parameterization, and protection against common OWASP Top 10 vulnerabilities.

---

## 🚀 Features & Security Controls

* **Authentication (JWT & Bcrypt):** Secure token-based user authentication using `jsonwebtoken` and password hashing with `bcryptjs` (salt rounds: 10).
* **Authorization (RBAC):** Role-Based Access Control ensuring strict separation of privileges between standard `user` accounts and `admin` accounts.
* **SQL Injection Prevention:** 100% prepared/parameterized queries across all database read and write operations.
* **Brute-Force Protection:** Rate limiting on authentication endpoints using `express-rate-limit`.
* **Security Headers:** HTTP headers hardened using `helmet` to mitigate cross-site scripting (XSS), clickjacking, and MIME-sniffing.

---

## 🛡️ OWASP Top 10 Mitigation Mapping

| OWASP Risk Category | Threat Prevented | Security Control Implemented |
| :--- | :--- | :--- |
| **A01:2021 - Broken Access Control** | Unauthorized privilege escalation / IDOR | JWT verification middleware + role authorization (`authorizeRoles('admin')`). |
| **A02:2021 - Cryptographic Failures** | Plaintext password leaks | `bcryptjs` salted hashing before saving credentials to the database. |
| **A03:2021 - Injection** | SQL Injection (SQLi) | Parameterized SQLite queries using input bindings (`?`). |
| **A07:2021 - Identification & Auth Failures** | Automated brute-force attacks | Express rate limiter restricting login requests (10 requests per 15 minutes per IP). |

---

## 🛠️ Tech Stack

* **Language & Runtime:** Node.js (v18+)
* **Framework:** Express.js
* **Database:** SQLite3
* **Security & Auth:** `bcryptjs`, `jsonwebtoken`, `helmet`, `express-rate-limit`, `dotenv`
* **Development Tools:** `nodemon`

---

## 📁 Directory Structure

```text
secure-web-app/
├── database.js          # SQLite connection and schema setup
├── server.js            # Express server initialization & security middleware
├── .env                 # Environment configuration (JWT secrets, Port)
├── .gitignore           # Ignored files (node_modules, .env, *.db)
├── package.json         # Project metadata and dependencies
├── README.md            # Project documentation
├── middleware/
│   ├── auth.js          # JWT verification & RBAC middleware
│   └── rateLimiter.js   # Rate limiting policy definition
└── routes/
    ├── auth.js          # Registration & Login endpoints
    └── tasks.js         # Protected task endpoints
```

---

## ⚡ Quick Start & Setup Guide

### 1. Prerequisites
* **Node.js** (v18.0.0 or higher)
* **npm** (v9.0.0 or higher)

### 2. Installation

Clone the repository and install dependencies:

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/secure-web-app.git
cd secure-web-app

# Install Node modules
npm install
```

### 3. Environment Configuration

Create a `.env` file in the root directory:

```env
PORT=3000
JWT_SECRET=super_secret_jwt_key_change_in_production
```

### 4. Running the Application

```bash
# Run in production mode
node server.js

# Run in development mode (with auto-reload)
npx nodemon server.js
```

The server will start at `http://localhost:3000`.

---

## 📡 API Reference & Testing

### Authentication Routes (`/api/auth`)

#### 1. Register User
* **Endpoint:** `POST /api/auth/register`
* **Headers:** `Content-Type: application/json`
* **Body:**
  ```json
  {
    "username": "swastik",
    "password": "UserPass123!",
    "role": "user"
  }
  ```
* **PowerShell Test Command:**
  ```powershell
  curl.exe -X POST http://localhost:3000/api/auth/register -H "Content-Type: application/json" -d '{"username": "swastik", "password": "UserPass123!", "role": "user"}'
  ```

#### 2. User Login
* **Endpoint:** `POST /api/auth/login`
* **Headers:** `Content-Type: application/json`
* **Body:**
  ```json
  {
    "username": "swastik",
    "password": "UserPass123!"
  }
  ```
* **PowerShell Test Command:**
  ```powershell
  curl.exe -X POST http://localhost:3000/api/auth/login -H "Content-Type: application/json" -d '{"username": "swastik", "password": "UserPass123!"}'
  ```
* **Response:**
  ```json
  {
    "message": "Login successful",
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }
  ```

---

### Task Routes (`/api/tasks`)

#### 3. Create Task (Authenticated User)
* **Endpoint:** `POST /api/tasks`
* **Headers:** `Authorization: Bearer <JWT_TOKEN>`, `Content-Type: application/json`
* **PowerShell Test Command:**
  ```powershell
  curl.exe -X POST http://localhost:3000/api/tasks -H "Content-Type: application/json" -H "Authorization: Bearer <YOUR_JWT_TOKEN>" -d '{"title": "Review OWASP Security Guidelines"}'
  ```

#### 4. Get User Tasks
* **Endpoint:** `GET /api/tasks`
* **Headers:** `Authorization: Bearer <JWT_TOKEN>`
* **PowerShell Test Command:**
  ```powershell
  curl.exe -X GET http://localhost:3000/api/tasks -H "Authorization: Bearer <YOUR_JWT_TOKEN>"
  ```

#### 5. Admin View All Tasks (RBAC Restricted)
* **Endpoint:** `GET /api/tasks/admin/all`
* **Headers:** `Authorization: Bearer <ADMIN_JWT_TOKEN>`
* **PowerShell Test Command:**
  ```powershell
  curl.exe -X GET http://localhost:3000/api/tasks/admin/all -H "Authorization: Bearer <YOUR_JWT_TOKEN>"
  ```
* *Note: Attempting this call with a standard `user` token will return HTTP status `403 Forbidden` (`{"error": "Unauthorized action"}`).*

---

## 🔒 Security Verification & Testing

To verify the implemented security controls:

1. **SQL Injection Check:** Input malicious strings (e.g., `' OR '1'='1`) into login parameters or task creation fields. The parameterized SQL engine treats them as literal string arguments, neutralizing the attack.
2. **Access Control (RBAC) Check:** Attempt to query `/api/tasks/admin/all` using a JWT token issued to a standard user account. Verify that a `403 Forbidden` status code is received.
3. **Rate Limiting Check:** Send more than 10 rapid login attempts within a 15-minute window to trigger `429 Too Many Requests`.

---

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.
