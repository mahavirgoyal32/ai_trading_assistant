import requests
from utils import MOCK_ALPACA, ALPACA_API_KEY, ALPACA_SECRET_KEY, ALPACA_BASE_URL

HEADERS = {
    "APCA-API-KEY-ID": ALPACA_API_KEY or "demo-key",
    "APCA-API-SECRET-KEY": ALPACA_SECRET_KEY or "demo-secret",
    "Content-Type": "application/json",
}


def place_order(action: str, ticker: str, quantity: int, order_type: str, limit_price: float | None):
    if MOCK_ALPACA:
        return {
            "mock": True,
            "status": "accepted",
            "id": "demo-order-123",
            "symbol": ticker,
            "side": action,
            "qty": quantity,
            "type": order_type,
            "limit_price": limit_price,
        }
    payload = {
        "symbol": ticker,
        "qty": quantity,
        "side": action,
        "type": order_type,
        "time_in_force": "gtc",
    }
    if order_type == "limit" and limit_price is not None:
        payload["limit_price"] = float(limit_price)

    url = f"{ALPACA_BASE_URL.rstrip('/')}/v2/orders"
    r = requests.post(url, json=payload, headers=HEADERS, timeout=15)
    r.raise_for_status()
    return r.json()
