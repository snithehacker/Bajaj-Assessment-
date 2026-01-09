from fastapi import FastAPI, HTTPException, Depends, Header, Request
from fastapi.responses import JSONResponse
import logging
from services.instrument_service import get_all_instruments
from services.order_service import place_order, get_order, cancel_order
from services.trade_service import get_all_trades
from services.portfolio_service import get_portfolio
from storage.in_memory_db import INSTRUMENTS

logging.basicConfig(level=logging.INFO)

app = FastAPI(title="Bajaj Trading SDK")

def verify_api_key(x_api_key: str = Header(None)):
    if x_api_key != "secret_key":
        raise HTTPException(status_code=401, detail="Invalid API key")
    return x_api_key

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logging.error(f"Unexpected error: {exc}")
    return JSONResponse(status_code=500, content={"detail": "Internal Server Error"})

@app.get("/api/v1/instruments", dependencies=[Depends(verify_api_key)])
def fetch_instruments():
    return get_all_instruments()

@app.post("/api/v1/orders", dependencies=[Depends(verify_api_key)])
def create_order(order: dict):
    try:
        return place_order(order)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/v1/orders/{order_id}", dependencies=[Depends(verify_api_key)])
def fetch_order(order_id: str):
    order = get_order(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@app.delete("/api/v1/orders/{order_id}", dependencies=[Depends(verify_api_key)])
def cancel_order_endpoint(order_id: str):
    try:
        return cancel_order(order_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/v1/trades", dependencies=[Depends(verify_api_key)])
def fetch_trades():
    return get_all_trades()

@app.get("/api/v1/portfolio", dependencies=[Depends(verify_api_key)])
def fetch_portfolio():
    return get_portfolio(INSTRUMENTS)