from storage.in_memory_db import PORTFOLIO
import logging

def update_portfolio(symbol, side, quantity, price, check_only=False):
    holding = PORTFOLIO.get(symbol)

    if side == "BUY":
        if check_only:
            return  # No check needed for buy
        if holding:
            total_cost = holding["averagePrice"] * holding["quantity"] + price * quantity
            new_qty = holding["quantity"] + quantity
            holding["averagePrice"] = total_cost / new_qty
            holding["quantity"] = new_qty
        else:
            PORTFOLIO[symbol] = {
                "symbol": symbol,
                "quantity": quantity,
                "averagePrice": price
            }
    elif side == "SELL":
        if not holding or holding["quantity"] < quantity:
            raise ValueError("Insufficient quantity to sell")
        if check_only:
            return  # Check passed
        holding["quantity"] -= quantity
        if holding["quantity"] <= 0:
            del PORTFOLIO[symbol]

    logging.info(f"Updated portfolio for {symbol}")

def get_portfolio(instruments):
    result = []
    for sym, holding in PORTFOLIO.items():
        ltp = next((i["lastTradedPrice"] for i in instruments if i["symbol"] == sym), None)
        if ltp is not None:
            result.append({
                "symbol": sym,
                "quantity": holding["quantity"],
                "averagePrice": holding["averagePrice"],
                "currentValue": holding["quantity"] * ltp
            })
    return result