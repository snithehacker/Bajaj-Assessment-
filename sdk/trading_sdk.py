import requests

class TradingSDK:
    def __init__(self, base_url="http://127.0.0.1:8000", api_key="secret_key"):
        self.base_url = base_url
        self.headers = {"X-API-KEY": api_key}

    def get_instruments(self):
        return requests.get(f"{self.base_url}/api/v1/instruments", headers=self.headers).json()

    def place_order(self, symbol, side, order_type, quantity, price=None):
        payload = {
            "symbol": symbol,
            "side": side,
            "orderType": order_type,
            "quantity": quantity,
            "price": price
        }
        return requests.post(f"{self.base_url}/api/v1/orders", json=payload, headers=self.headers).json()

    def get_order(self, order_id):
        return requests.get(f"{self.base_url}/api/v1/orders/{order_id}", headers=self.headers).json()

    def cancel_order(self, order_id):
        return requests.delete(f"{self.base_url}/api/v1/orders/{order_id}", headers=self.headers).json()

    def get_trades(self):
        return requests.get(f"{self.base_url}/api/v1/trades", headers=self.headers).json()

    def get_portfolio(self):
        return requests.get(f"{self.base_url}/api/v1/portfolio", headers=self.headers).json()