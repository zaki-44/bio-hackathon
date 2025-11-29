import requests
import json

BASE_URL = "http://127.0.0.1:5000/api"

def test_api():
    print("Testing Delivery API...")
    
    # 1. Login
    session = requests.Session()
    login_res = session.post(f"{BASE_URL}/login", json={
        "username": "transporter1",
        "password": "password"
    })
    
    if login_res.status_code != 200:
        print(f"Login failed: {login_res.text}")
        return
        
    print("Login successful")
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # 2. Get Packages
    # Note: The current implementation uses session for auth in some places and JWT in others?
    # Let's check the code. auth.py uses session AND returns token.
    # delivery.py checks session.get('logged_in').
    # This means we need to use the session cookie.
    
    packages_res = session.get(f"{BASE_URL}/delivery/packages")
    if packages_res.status_code != 200:
        print(f"Get packages failed: {packages_res.text}")
        return
        
    packages = packages_res.json()["packages"]
    print(f"Fetched {len(packages)} packages")
    
    if not packages:
        print("No packages found to update")
        return

    # 3. Update Status
    pkg = packages[0]
    pkg_id = pkg["id"]
    print(f"Updating package {pkg_id} ({pkg['tracking_number']})...")
    
    update_res = session.put(f"{BASE_URL}/delivery/packages/{pkg_id}/status", json={
        "status": "picked_up"
    })
    
    if update_res.status_code != 200:
        print(f"Update failed: {update_res.text}")
        return
        
    print("Update successful")
    print(json.dumps(update_res.json(), indent=2))

if __name__ == "__main__":
    test_api()
