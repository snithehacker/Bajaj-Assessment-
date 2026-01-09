from storage.in_memory_db import TRADES
import logging

def add_trade(trade):
    TRADES.append(trade)
    logging.info(f"Added trade {trade['tradeId']}")

def get_all_trades():
    return TRADES