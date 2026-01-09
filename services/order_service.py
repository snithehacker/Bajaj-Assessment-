import uuid
from datetime import datetime
import logging
from storage.in_memory_db import ORDERS
from services.instrument_service import get_instrument_by_symbol
from services.trade_service import add_trade
from services.portfolio_service import update_portfolio

def place_order(data):
    if data["quantity"] <= 0:
        raise ValueError("Quantity must be greater than 0")

    if data["orderType"] == "LIMIT" and not data.get("price"):
        raise ValueError("Price is required for LIMIT orders")

    instrument = get_instrument_by_symbol(data["symbol"])
    if not instrument:
        raise ValueError("Invalid instrument symbol")

    order_id = str(uuid.uuid4())
    order = {
        "orderId": order_id,
        "symbol": data["symbol"],
        "side": data["side"],
        "orderType": data["orderType"],
        "quantity": data["quantity"],
        "price": data.get("price"),
        "status": "NEW",
        "timestamp": datetime.utcnow()
    }

    # Execution Logic
    ltp = instrument["lastTradedPrice"]

    if data["side"] == "SELL":
        # Check portfolio before proceeding
        try:
            update_portfolio(data["symbol"], data["side"], data["quantity"], ltp, check_only=True)
        except ValueError as e:
            raise e

    if data["orderType"] == "MARKET" or (data["orderType"] == "LIMIT" and data["price"] == ltp):
        order["status"] = "EXECUTED"
        trade = {
            "tradeId": str(uuid.uuid4()),
            "orderId": order_id,
            "symbol": data["symbol"],
            "side": data["side"],
            "quantity": data["quantity"],
            "price": ltp,
            "timestamp": datetime.utcnow()
        }
        add_trade(trade)
        update_portfolio(data["symbol"], data["side"], data["quantity"], ltp)
    else:
        order["status"] = "PLACED"

    ORDERS[order_id] = order
    logging.info(f"Placed order {order_id} for {data['symbol']}")
    return order

def get_order(order_id):
    return ORDERS.get(order_id)

def cancel_order(order_id):
    order = ORDERS.get(order_id)
    if not order:
        raise ValueError("Order not found")
    if order["status"] in ["EXECUTED", "CANCELLED"]:
        raise ValueError("Cannot cancel already executed or cancelled order")
    order["status"] = "CANCELLED"
    logging.info(f"Cancelled order {order_id}")
    return order