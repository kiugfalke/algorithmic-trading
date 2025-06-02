# trade_strategy.py
import pandas as pd

from data_loader import get_market_data
from scripts.technical_analysis import calculate_rsi, calculate_macd

def generate_trade_signal(data):
    """ Genera señales de compra/venta basado en RSI, MACD y volumen """
    price_data = data["Close"]
    volume_data = data["Volume_Approx"]

    rsi = calculate_rsi(price_data)
    macd, signal_line = calculate_macd(price_data)
    avg_volume = volume_data.rolling(window=3).mean()  # 🔄 Promedio de volumen más sensible

    # 🔄 Confirmamos si el volumen está por encima del promedio en un 30%
    high_volume = volume_data.iloc[-1] > avg_volume.iloc[-1] * 1.3  

    # Aplicamos condiciones optimizadas para compra/venta
    if rsi.iloc[-1] > 70 and macd.iloc[-1] < signal_line.iloc[-1] and high_volume:
        return "🔴 Vender (Confirmado con alto volumen)"
    elif rsi.iloc[-1] < 30 and macd.iloc[-1] > signal_line.iloc[-1] and high_volume:
        return "🟢 Comprar (Confirmado con alto volumen)"
    return "⚪ Mantener"

if __name__ == "__main__":
    market_data = get_market_data("EURUSD=X")
    signal = generate_trade_signal(market_data)
    print("📊 Señal optimizada con volumen:", signal)

import matplotlib.pyplot as plt
from data_loader import get_market_data

# Obtener datos de mercado en tiempo real
market_data = get_market_data("EURUSD=X")

# Generar la señal de trading
signal = generate_trade_signal(market_data)
print("Señal optimizada con volumen:", signal)

# 📊 Graficar precios y volumen
plt.figure(figsize=(12, 6))

# 🔵 Gráfico de precio de cierre
plt.subplot(2, 1, 1)
plt.plot(market_data["Close"], label="Precio de cierre", color="blue")
plt.title("Precio y Volumen de EUR/USD")
plt.legend()

# ⚫ Gráfico de volumen
plt.subplot(2, 1, 2)
plt.bar(market_data.index, market_data["Volume_Approx"], label="Volatilidad (aprox. volumen)", color="gray")
plt.legend()

plt.show()