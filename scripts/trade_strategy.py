# trade_strategy.py
from scripts.technical_analysis import calculate_rsi

# Usar el RSI para generar señales
def generate_trade_signal(data):
    rsi = calculate_rsi(data)
    if rsi.iloc[-1] > 70:
        return "Vender"
    elif rsi.iloc[-1] < 30:
        return "Comprar"
    return "Mantener"