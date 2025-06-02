import yfinance as yf
import pandas as pd

def get_market_data(ticker, period="30d", interval="1h"):
    """ Obtiene precios y estima actividad de mercado con volatilidad """
    data = yf.download(ticker, period=period, interval=interval)
    
    # 🔄 Sustituimos volumen real por una métrica basada en volatilidad
    data["Volume_Approx"] = data["High"] - data["Low"]  
    return data[["Close", "Volume_Approx"]]  # 📊 Retornamos precios y actividad estimada

if __name__ == "__main__":
    market_data = get_market_data("EURUSD=X")
    print(market_data.tail())  # 🔍 Ver últimos valores