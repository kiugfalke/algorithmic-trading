import pandas as pd
from data_loader import get_market_data
from imf_data_extraction import fetch_imf_data
from fundamental_analysis import fetch_forex_events
from sentiment_analysis import fetch_twitter_sentiment, fetch_news_sentiment
from technical_analysis import calculate_rsi, calculate_macd

def generate_trade_signal():
    """ Genera señales de compra/venta integrando análisis técnico, fundamental y sentimiento """
    market_data = get_market_data("EURUSD=X")
    macro_data = fetch_imf_data("US")
    economic_events = fetch_forex_events()
    twitter_sentiment = fetch_twitter_sentiment()
    news_sentiment = fetch_news_sentiment()

    # Análisis técnico
    price_data = market_data["Close"]
    rsi = calculate_rsi(price_data)
    macd, signal_line = calculate_macd(price_data)
    
    # Evaluación de sentimiento y fundamental
    avg_sentiment = (twitter_sentiment["score"].mean() + news_sentiment["score"].mean()) / 2
    inflation_rate = macro_data[macro_data["Indicator"] == "PCPI_IX"]["Value"].iloc[-1]

    # Definir estrategia basada en condiciones combinadas
    if rsi.iloc[-1] > 70 and macd.iloc[-1] < signal_line.iloc[-1] and avg_sentiment < -0.2:
        return "🔴 Vender (Confirmado por sentimiento negativo e inflación alta)"
    elif rsi.iloc[-1] < 30 and macd.iloc[-1] > signal_line.iloc[-1] and avg_sentiment > 0.2:
        return "🟢 Comprar (Sentimiento positivo y condiciones macro favorables)"
    
    return "⚪ Mantener"

if __name__ == "__main__":
    signal = generate_trade_signal()
    print("📊 Señal de Trading:", signal)