import requests
import json
from kivy.network.urlrequest import UrlRequest
from kivy.app import App
from functools import partial

# Default to local server for testing. 
# In production, this should be the IP address of the server (e.g., http://192.168.1.X:5000/api)
BASE_URL = "http://127.0.0.1:5000/api"

class APIClient:
    def __init__(self):
        self.base_url = BASE_URL
        self.headers = {'Content-Type': 'application/json'}

    # --- Synchronous Wrapper (Not recommended for UI, but for simplicity in migration) ---
    # Note: For a smooth UI, we should use UrlRequest (Async), but to minimize refactoring 
    # of the synchronous logic in screens.py, we'll use requests for now. 
    # Ideally, we should refactor screens.py to handle async callbacks.
    
    def get_categories(self):
        try:
            response = requests.get(f"{self.base_url}/categories")
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(f"Error fetching categories: {e}")
        return []

    def get_products(self, category_name=None):
        try:
            url = f"{self.base_url}/products"
            params = {}
            if category_name:
                params['category'] = category_name
            
            response = requests.get(url, params=params)
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(f"Error fetching products: {e}")
        return []

    def get_ads(self):
        try:
            response = requests.get(f"{self.base_url}/ads")
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(f"Error fetching ads: {e}")
        return []

    def get_offers(self):
        try:
            response = requests.get(f"{self.base_url}/offers")
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(f"Error fetching offers: {e}")
        return []

    def login(self, username, password):
        try:
            payload = {'username': username, 'password': password}
            response = requests.post(f"{self.base_url}/login", json=payload)
            if response.status_code == 200:
                return response.json()
        except:
            pass
        return None

    def add_product(self, name, price, category_name):
        try:
            payload = {
                'name': name,
                'price': float(price),
                'category': category_name
            }
            requests.post(f"{self.base_url}/products", json=payload)
            return True
        except:
            return False

    def add_category(self, name, icon):
        try:
            payload = {'name': name, 'icon': icon}
            response = requests.post(f"{self.base_url}/categories", json=payload)
            return response.status_code == 201
        except:
            return False

    def add_ad(self, title, description):
        try:
            payload = {'title': title, 'description': description}
            requests.post(f"{self.base_url}/ads", json=payload)
            return True
        except:
            return False

    def delete_ad(self, ad_id):
        try:
            requests.delete(f"{self.base_url}/ads/{ad_id}")
            return True
        except:
            return False

    def add_offer(self, title, discount):
        try:
            payload = {'title': title, 'discount': discount}
            requests.post(f"{self.base_url}/offers", json=payload)
            return True
        except:
            return False

    def delete_offer(self, offer_id):
        try:
            requests.delete(f"{self.base_url}/offers/{offer_id}")
            return True
        except:
            return False

    def add_order(self, total_amount, items_count):
        try:
            payload = {'total_amount': total_amount, 'items_count': items_count}
            requests.post(f"{self.base_url}/orders", json=payload)
            return True
        except:
            return False

    def get_stats(self):
        try:
            response = requests.get(f"{self.base_url}/stats")
            if response.status_code == 200:
                return response.json()
        except:
            pass
        return {
            'categories_count': 0,
            'products_count': 0,
            'orders_count': 0,
            'ads_count': 0,
            'offers_count': 0,
            'products_per_category': []
        }
