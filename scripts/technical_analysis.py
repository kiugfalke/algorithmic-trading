# technical_analysis.py
import pandas as pd
import numpy as np

def calculate_rsi(data, period=14):
    """ Calcula el RSI con base en los precios """
    delta = data.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi