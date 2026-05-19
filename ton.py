import requests

CLIENT_ID = 'e4e779dfc978380709f8914dd18e092c'
CLIENT_SECRET = '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'
SHOP_NAME = 'messy-merchant-lab'


def get_shopify_token():
    url = f"https://{SHOP_NAME}.myshopify.com/admin/oauth/access_token"

    payload = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "client_credentials"
    }

    try:
        response = requests.post(url, data=payload)
        response.raise_for_status()
        token_data = response.json()
        return token_data.get("access_token")
    except Exception as e:
        print(f"Error fetching token: {e}")
        return None


token = get_shopify_token()
if token:
    print(f"Token found: {token}")
else:
    print("Token not found")