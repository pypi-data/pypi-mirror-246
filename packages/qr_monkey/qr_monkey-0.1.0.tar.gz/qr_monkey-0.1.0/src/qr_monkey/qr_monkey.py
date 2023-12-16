import requests


base_url = "https://api.qrcode-monkey.com"

class QrCodeMonkeyAPI:
    def __init__(self):
        self.base_url = base_url

    def create_custom_qr_code(self, params):
        endpoint = "/qr/custom"
        payload = params
        return self._make_request(endpoint, payload)


    def _make_request(self, endpoint, payload):
        url = self.base_url + endpoint
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, json=payload, headers=headers)

        if response.status_code == 200:
            return response.content
        else:
            print(f"Error: {response.status_code}")
            return None

def custom(params):
    qr_api = QrCodeMonkeyAPI()
    qr_code = qr_api.create_custom_qr_code(params)

    if qr_code:
        with open('custom_qr_code.png', 'wb') as f:
            f.write(qr_code)
        print("Custom QR code created successfully.")
    else:
        print("Error creating custom QR code.")


# Example usage
if __name__ == "__main__":
    params = {
        "data": base_url,
            "config": {
                "body": "circle",
            },
            "size": 300,
            "download": False,
            "file": "png"
    }


    custom(params)
   