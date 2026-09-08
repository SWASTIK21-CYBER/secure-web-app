from functools import wraps
import datetime
import os
import sqlite3
import bcrypt
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import jwt

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Static secret key ensures tokens remain valid across server restarts
SECRET_KEY = os.getenv(
    "JWT_SECRET", "super_secret_key_that_is_at_least_32_bytes_long_123456"
)
DATABASE = "database.db"

# Setup Rate Limiting (OWASP Protection: Prevents Brute Force Attacks)
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://",
)

# ----------------------------------------------------
# DATABASE SETUP
# ----------------------------------------------------


def get_db():
  """Establish database connection with Row factory for dict-like access."""
  conn = sqlite3.connect(DATABASE)
  conn.row_factory = sqlite3.Row
  return conn


def init_db():
  """Initialize database schema on startup."""
  conn = get_db()
  cursor = conn.cursor()
  cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'user'
        )
    """)
  conn.commit()
  conn.close()


init_db()

# ----------------------------------------------------
# SECURITY DECORATORS (Middleware Equivalent)
# ----------------------------------------------------


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization")

        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"error": "Authorization token missing or invalid"}), 401

        token = auth_header.split(" ")[1]

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            request.current_user = payload
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token has expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401

        return f(*args, **kwargs)

    return decorated


def role_required(required_role):
  """Decorator for Role-Based Access Control (RBAC)."""

  def decorator(f):

    @wraps(f)
    def decorated(*args, **kwargs):
      user = getattr(request, "current_user", None)
      if not user or user.get("role") != required_role:
        return (
            jsonify({"error": "Forbidden: Insufficient permissions"}),
            403,
        )
      return f(*args, **kwargs)

    return decorated

  return decorator


# ----------------------------------------------------
# ROUTES & ENDPOINTS
# ----------------------------------------------------


@app.route("/")
def home():
  """Root endpoint to check API health."""
  return jsonify({
      "status": "Online",
      "message": "Secure Web Application API is running successfully",
  })


@app.route("/register", methods=["POST"])
def register():
  """User Registration Route with SQL Injection Defense & Bcrypt Hashing."""
  data = request.get_json() or {}
  username = data.get("username")
  password = data.get("password")
  role = data.get("role", "user")

  if not username or not password:
    return jsonify({"error": "Username and password required"}), 400

  # OWASP Security: Securely hash password with salt
  hashed_password = bcrypt.hashpw(
      password.encode("utf-8"), bcrypt.gensalt()
  ).decode("utf-8")

  conn = get_db()
  cursor = conn.cursor()

  try:
    # OWASP Security: Parameterized Query prevents SQL Injection
    cursor.execute(
        "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
        (username, hashed_password, role),
    )
    conn.commit()
  except sqlite3.IntegrityError:
    return jsonify({"error": "Username already exists"}), 409
  finally:
    conn.close()

  return jsonify({"message": "User registered successfully"}), 201


@app.route("/login", methods=["POST"])
@limiter.limit("5 per minute")
def login():
  data = request.get_json() or {}
  username = data.get("username")
  password = data.get("password")

  if not username or not password:
    return jsonify({"error": "Username and password required"}), 400

  conn = get_db()
  cursor = conn.cursor()
  cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
  user = cursor.fetchone()
  conn.close()

  if user and bcrypt.checkpw(
      password.encode("utf-8"), user["password"].encode("utf-8")
  ):
    token_payload = {
        "sub": str(user["id"]),  # <-- CAST TO str() HERE TO FIX "Subject must be a string"
        "username": user["username"],
        "role": user["role"],
        "exp": datetime.datetime.now(datetime.timezone.utc)
        + datetime.timedelta(hours=2),
    }

    token = jwt.encode(token_payload, SECRET_KEY, algorithm="HS256")

    if isinstance(token, bytes):
      token = token.decode("utf-8")

    return jsonify({"token": token}), 200
  else:
    return jsonify({"error": "Invalid username or password"}), 401


@app.route("/profile", methods=["GET"])
@token_required
def profile():
  """Protected Route: Accessible by any authenticated user."""
  user = request.current_user
  return jsonify({
      "message": "Access granted to protected route",
      "user": {
          "id": user["sub"],
          "username": user["username"],
          "role": user["role"],
      },
  })


@app.route("/admin", methods=["GET"])
@token_required
@role_required("admin")
def admin_only():
  """Protected Route: Accessible ONLY by users with 'admin' role."""
  return jsonify(
      {"message": "Welcome to the Admin Dashboard!", "status": "Secure Access"}
  )


if __name__ == "__main__":
  app.run(debug=True, host="127.0.0.1", port=5000)