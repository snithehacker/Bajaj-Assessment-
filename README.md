# Bajaj Trading SDK Assignment

This is a simplified Trading API backend and SDK wrapper built with Python, FastAPI, and in-memory storage. It simulates core trading workflows without real market integration.

## Setup and Run Instructions
1. Clone repo: `git clone https://github.com/snithehacker/Bajaj-Assessment-`
2. Create virtual env: `python -m venv venv; source venv/bin/activate` (or `venv\Scripts\activate` on Windows)
3. Install deps: `pip install -r requirements.txt`
4. Run server: `uvicorn app:app --reload`
5. Access APIs at http://127.0.0.1:8000 (Swagger docs at /docs)
6. Use SDK: See sdk/trading_sdk.py for client methods. Init with `sdk = TradingSDK(api_key="secret_key")`

## API Details
- GET /api/v1/instruments: List instruments
- POST /api/v1/orders: Place order (body: {"symbol": str, "side": "BUY/SELL", "orderType": "MARKET/LIMIT", "quantity": int, "price": float?})
- GET /api/v1/orders/{order_id}: Get order status
- DELETE /api/v1/orders/{order_id}: Cancel order
- GET /api/v1/trades: List trades
- GET /api/v1/portfolio: Get holdings
All require header `X-API-KEY: secret_key` (mock auth).

## Assumptions
- Single user (mock auth).
- Immediate execution for market orders or limit if price == LTP.
- In-memory DB resets on restart.
- No real-time matching; simple simulation.
- Error handling for invalid inputs, insufficient sell quantity.

## Bonus Features
- Logging and global exception handling.
- Unit tests (run `pytest`).
- Swagger docs (/docs).
- Cancel order support.
- Docker support (see Dockerfile).

## Sample Usage

See samples.txt for curl examples.
