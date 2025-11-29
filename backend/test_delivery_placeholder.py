import requests
import json

BASE_URL = "http://localhost:5000/api"

def test_delivery_flow():
    print("Starting delivery flow test...")
    
    # 1. Register a transporter
    transporter_data = {
        "username": "transporter_test",
        "email": "transporter@test.com",
        "password": "password123",
        "user_type": "transporter"
    }
    
    # Try login first to see if user exists
    login_response = requests.post(f"{BASE_URL}/login", json={
        "username": transporter_data["username"],
        "password": transporter_data["password"]
    })
    
    if login_response.status_code == 200:
        print("User already exists, logging in...")
        token = login_response.json()["access_token"]
        user_id = login_response.json()["user"]["id"]
    else:
        print("Registering new transporter...")
        reg_response = requests.post(f"{BASE_URL}/register", json=transporter_data)
        if reg_response.status_code != 201:
            print(f"Registration failed: {reg_response.text}")
            return
        token = reg_response.json()["access_token"]
        user_id = reg_response.json()["user"]["id"]

    headers = {"Authorization": f"Bearer {token}"}
    
    # 2. Create a package (Direct DB insertion needed as there is no public API for this yet)
    # For this test, we'll assume the package exists or we need a way to create it.
    # Since I can't easily run python code to insert into DB from here without a script, 
    # I will create a temporary route in app.py or just use the fact that I can't easily test this 
    # without a seed script. 
    
    # Wait, I can create a seed script and run it via `run_command`.
    # Let's do that instead of this pure python request script.
    pass

if __name__ == "__main__":
    test_delivery_flow()
