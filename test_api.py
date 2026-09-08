import requests

BASE_URL = "http://127.0.0.1:5000"

# 1. Login
login_res = requests.post(
    f"{BASE_URL}/login", json={"username": "swastik", "password": "myPassword213"}
)

if login_res.status_code == 200:
  token = login_res.json().get("token")
  print("✓ Login successful. Token received.")

  # 2. Access Profile
  headers = {"Authorization": f"Bearer {token}"}
  profile_res = requests.get(f"{BASE_URL}/profile", headers=headers)
  print("Profile Response:", profile_res.json())
else:
  print("x Login failed:", login_res.json())