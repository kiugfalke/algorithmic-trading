import pandas as pd
import numpy as np

def calculate_rsi(data, period=8):
    """ Calcula el Índice de Fuerza Relativa (RSI) con suavizado exponencial """
    data = data.squeeze()
    delta = data.diff()
    
    gain = np.where(delta > 0, delta, 0)
    loss = np.where(delta < 0, -delta, 0)
    
    avg_gain = pd.Series(gain).ewm(span=period, adjust=False).mean()
    avg_loss = pd.Series(loss).ewm(span=period, adjust=False).mean()
    
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return pd.Series(rsi, index=data.index)

def calculate_macd(data, short_period=12, long_period=26, signal_period=9):
    """ Calcula el MACD con períodos más tradicionales """
    short_ema = data.ewm(span=short_period, adjust=False).mean()
    long_ema = data.ewm(span=long_period, adjust=False).mean()
    
    macd = short_ema - long_ema
    signal = macd.ewm(span=signal_period, adjust=False).mean()
    
    return macd, signal

def calculate_obv(prices, volumes):
    """ Calcula el On-Balance Volume (OBV) """
    obv = [0]  
    for i in range(1, len(prices)):
        if prices[i] > prices[i - 1]:
            obv.append(obv[-1] + volumes[i])
        elif prices[i] < prices[i - 1]:
            obv.append(obv[-1] - volumes[i])
        else:
            obv.append(obv[-1])
    
    return pd.Series(obv, index=prices.index)

# Validación rápida
if __name__ == "__main__":
    sample_prices = pd.Series([100, 102, 104, 103, 105, 108, 107, 109, 111, 113, 115, 117, 119, 121, 123])
    sample_volumes = pd.Series([500, 600, 800, 700, 650, 900, 1000, 1100, 1050, 1200, 1300, 1250, 1350, 1400, 1500])
    
    print("RSI:\n", calculate_rsi(sample_prices))
    print("MACD:\n", calculate_macd(sample_prices)[0])  # Solo MACD, sin línea de señal
    print("OBV:\n", calculate_obv(sample_prices, sample_volumes))