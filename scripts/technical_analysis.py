# technical_analysis.py
import pandas as pd
import numpy as np

def calculate_rsi(data, period=8):
    """ Calcula el Índice de Fuerza Relativa (RSI) basado en precios """
    data = data.squeeze()  # Convierte el DataFrame a una serie unidimensional
    
    delta = data.diff()
    gain = np.where(delta > 0, delta, 0)
    loss = np.where(delta < 0, -delta, 0)
    
    avg_gain = pd.Series(gain).rolling(window=period, min_periods=1).mean()
    avg_loss = pd.Series(loss).rolling(window=period, min_periods=1).mean()
    
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return pd.Series(rsi, index=data.index)

def calculate_macd(data, short_period=9, long_period=21, signal_period=6):  # 🔄 Más reactivo a cambios bruscos
    """ Calcula el MACD y su línea de señal """
    short_ema = data.ewm(span=short_period, adjust=False).mean()
    long_ema = data.ewm(span=long_period, adjust=False).mean()
    
    macd = short_ema - long_ema
    signal = macd.ewm(span=signal_period, adjust=False).mean()
    
    return macd, signal

def calculate_moving_average(data, period=5):
    return data.rolling(window=period, min_periods=1).mean()

# Validación rápida
if __name__ == "__main__":
    # Datos de ejemplo
    sample_data = pd.Series([100, 102, 104, 103, 105, 108, 107, 109, 111, 113, 115, 117, 119, 121, 123])
    
    print("RSI:\n", calculate_rsi(sample_data))
    print("MACD:\n", calculate_macd(sample_data)[0])  # Solo MACD, sin línea de señal
    print("Media Móvil:\n", calculate_moving_average(sample_data))