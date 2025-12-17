import requests
import json
import time
from threading import Thread
from app import app

# Start server in a separate thread
def start_server():
    app.run(port=5001)

server_thread = Thread(target=start_server, daemon=True)
server_thread.start()
time.sleep(2) # Wait for server to start

BASE_URL = 'http://127.0.0.1:5001/api'

def test_api():
    print("Testing API...")
    
    # 1. Login
    print("\n1. Testing Login...")
    login_data = {'username': 'admin', 'password': 'admin123'}
    try:
        res = requests.post(f'{BASE_URL}/login', json=login_data)
        if res.status_code == 200:
            print("Login Successful")
        else:
            print(f"Login Failed: {res.status_code} - {res.text}")
    except Exception as e:
        print(f"Login Error: {e}")

    # 2. Get Categories
    print("\n2. Testing Get Categories...")
    try:
        res = requests.get(f'{BASE_URL}/categories')
        if res.status_code == 200:
            cats = res.json()
            print(f"Got {len(cats)} categories")
            if len(cats) > 0:
                print(f"   Sample: {cats[0]['name']}")
        else:
            print(f"Get Categories Failed: {res.status_code}")
    except Exception as e:
        print(f"Get Categories Error: {e}")

    # 3. Add Product
    print("\n3. Testing Add Product...")
    product_data = {
        'name': 'Test Product',
        'price': 100,
        'category': 'أقلام', # Assuming this category exists from init_db
        'image': 'test.jpg'
    }
    try:
        res = requests.post(f'{BASE_URL}/products', json=product_data)
        if res.status_code == 201:
            print("Add Product Successful")
        else:
            print(f"Add Product Failed: {res.status_code} - {res.text}")
    except Exception as e:
        print(f"Add Product Error: {e}")

    # 4. Get Products
    print("\n4. Testing Get Products...")
    try:
        res = requests.get(f'{BASE_URL}/products')
        if res.status_code == 200:
            products = res.json()
            print(f"Got {len(products)} products")
            found = False
            for p in products:
                if p['name'] == 'Test Product':
                    found = True
                    print(f"   Found created product: {p['name']} - Category: {p['category']}")
                    break
            if not found:
                print("Created product not found in list")
        else:
            print(f"Get Products Failed: {res.status_code}")
    except Exception as e:
        print(f"Get Products Error: {e}")

if __name__ == '__main__':
    test_api()
