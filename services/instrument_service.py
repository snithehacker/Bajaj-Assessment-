from storage.in_memory_db import INSTRUMENTS

def get_all_instruments():
    return INSTRUMENTS

def get_instrument_by_symbol(symbol: str):
    for inst in INSTRUMENTS:
        if inst["symbol"] == symbol:
            return inst
    return None