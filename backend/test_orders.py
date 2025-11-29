import requests
import json

BASE_URL = "http://localhost:5000/api"

def test_orders():
    session = requests.Session()
    
    # 1. Login
    print("Logging in...")
    login_data = {
        "username": "farmer_john",
        "password": "password"
    }
    response = session.post(f"{BASE_URL}/login", json=login_data)
    if response.status_code != 200:
        print(f"Login failed: {response.text}")
        return
    print("Login successful")
    
    # 2. Get Products to add to cart
    print("Fetching products...")
    response = session.get(f"{BASE_URL}/products")
    try:
        products = response.json().get('products', [])
    except json.JSONDecodeError:
        print(f"Failed to decode JSON. Status: {response.status_code}")
        print(f"Response text: {response.text[:500]}")
        return

    if not products:
        print("No products found")
        return
        
    product = products[0]
    print(f"Selected product: {product['name']} (ID: {product['id']})")
    
    # 3. Create Order
    print("Creating order...")
    cart_items = [
        {
            "id": product['id'],
            "quantity": 2
        }
    ]
    
    response = session.post(f"{BASE_URL}/orders", json={"items": cart_items})
    if response.status_code == 201:
        order = response.json().get('order')
        print(f"Order created successfully! Order ID: {order['id']}")
        print(f"Total Amount: {order['total_amount']}")
        print(f"Status: {order['status']}")
    else:
        print(f"Failed to create order: {response.text}")
        return

    # 4. Get Orders
    print("Fetching user orders...")
    response = session.get(f"{BASE_URL}/orders")
    if response.status_code == 200:
        orders = response.json().get('orders', [])
        print(f"Found {len(orders)} orders")
        for o in orders:
            print(f"- Order #{o['id']}: {o['total_amount']} ({o['status']})")
    else:
        print(f"Failed to fetch orders: {response.text}")

if __name__ == "__main__":
    test_orders()
