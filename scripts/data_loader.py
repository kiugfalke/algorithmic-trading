import yfinance as yf
import pandas as pd

def get_market_data(ticker, period="30d", interval="1h"):
    """ Obtiene precios, volatilidad y volumen real con ajustes para análisis técnico y fundamental """
    try:
        data = yf.download(ticker, period=period, interval=interval, timeout=10)
        
        if data.empty:
            raise ValueError("No se encontraron datos para el ticker proporcionado.")

        # Cálculo de volatilidad real con Average True Range (ATR)
        data["ATR"] = (data["High"] - data["Low"]).rolling(window=5).mean()

        # Normalización del ATR
        data["ATR_Norm"] = (data["ATR"] - data["ATR"].min()) / (data["ATR"].max() - data["ATR"].min())

        # Incorporamos volumen real si está disponible
        if "Volume" in data.columns:
            data["Volume_Real"] = data["Volume"]
        else:
            data["Volume_Real"] = data["ATR"] * 1000  # 🔄 Estimación basada en volatilidad

        return data[["Close", "ATR", "ATR_Norm", "Volume_Real"]]

    except Exception as e:
        print(f"Error al obtener datos: {e}")
        return pd.DataFrame()

if __name__ == "__main__":
    market_data = get_market_data("EURUSD=X")
    print(market_data.tail())  # 🔍 Ver últimos valores