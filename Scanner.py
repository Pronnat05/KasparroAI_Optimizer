# scanner.py
import requests
import os
from dotenv import load_dotenv

load_dotenv()

class ShopifyScanner:
    def __init__(self):
        self.shop_name = os.getenv("SHOP_NAME")
        self.token = os.getenv("SHOPIFY_ACCESS_TOKEN")
        self.url = f"https://{self.shop_name}.myshopify.com/admin/api/2026-04/graphql.json"
        self.headers = {
            "X-Shopify-Access-Token": self.token,
            "Content-Type": "application/json"
        }

    def fetch_products(self):
        query = """
        {
          products(first: 10) {
            edges {
              node {
                id
                title
                description
                vendor
              }
            }
          }
          shop {
            name
          }
        }
        """
        response = requests.post(self.url, json={'query': query}, headers=self.headers)
        res_json = response.json()
        if 'data' in res_json:
            return res_json['data']
        else:
            print("--- SHOPIFY ERROR RESPONSE ---")
            print(res_json)
            return None

if __name__ == "__main__":
    scanner = ShopifyScanner()
    print(scanner.fetch_products())