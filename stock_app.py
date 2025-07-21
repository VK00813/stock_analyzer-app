# stock_app.py
import streamlit as st
import yfinance as yf
import plotly.graph_objs as go
import pandas as pd
import ta

st.set_page_config(page_title="Stock Analyzer", layout="wide")
st.title("📈 Stock Analysis App")

ticker = st.text_input("Enter Stock Symbol (e.g., RELIANCE.NS):", "RELIANCE.NS")

if ticker:
    stock = yf.Ticker(ticker)
    df = stock.history(period="6mo")

    if df.empty:
        st.error("No data found. Please check the symbol.")
    else:
        st.subheader(f"📊 Current Price: ₹{stock.info.get('currentPrice', 'N/A')}")
        df['RSI'] = ta.momentum.RSIIndicator(df['Close']).rsi()
        df['MACD'] = ta.trend.MACD(df['Close']).macd()
        df['MA20'] = df['Close'].rolling(window=20).mean()

        st.write("### 🧠 Buy/Sell Suggestion:")
        rsi = df['RSI'].iloc[-1]
        macd = df['MACD'].iloc[-1]
        if rsi < 30 and macd > 0:
            st.success("📈 Suggestion: BUY - Oversold & bullish signal.")
        elif rsi > 70 and macd < 0:
            st.error("📉 Suggestion: SELL - Overbought & bearish signal.")
        else:
            st.warning("⏸ Suggestion: HOLD - Neutral indicators.")

        st.write("### 📉 Candlestick Chart")
        fig = go.Figure(data=[go.Candlestick(
            x=df.index,
            open=df['Open'],
            high=df['High'],
            low=df['Low'],
            close=df['Close']
        )])
        st.plotly_chart(fig, use_container_width=True)

        st.write("### 📈 Close Price with MA20")
        st.line_chart(df[['Close', 'MA20']])

        st.write("### 📍 RSI & MACD")
        st.line_chart(df[['RSI', 'MACD']])

        st.write("### 📰 News Headlines")
        try:
            for news in stock.news[:5]:
                st.markdown(f"- [{news['title']}]({news['link']})")
        except:
            st.info("No news available.")