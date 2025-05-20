from fastapi import APIRouter, HTTPException
from pymongo import MongoClient
import yfinance as yf
import pandas as pd
from ta import add_all_ta_features
import requests
from io import StringIO
from sklearn.ensemble import RandomForestClassifier
import numpy as np

router = APIRouter()

# MongoDB client setup
client = MongoClient("mongodb://localhost:27017/")
db = client["stock_data"]
stocks_collection = db["stocks"]

@router.get("/stocks/{ticker}")
def get_stock_data(ticker: str):
    # Check if data exists in the database
    stock_data = stocks_collection.find_one({"ticker": ticker})
    if stock_data:
        return stock_data

    # Try fetching data from yfinance
    try:
        df = yf.download(ticker, period="1mo", interval="1d")
        if not df.empty:
            df.reset_index(inplace=True)
            data = df.to_dict(orient="records")
            stocks_collection.insert_one({"ticker": ticker, "data": data})
            return {"ticker": ticker, "data": data}
    except Exception as e:
        print(f"Error fetching data from yfinance: {e}")

    # If yfinance fails, try other sources (Alpha Vantage, stooq.pl)
    # Placeholder for additional data sources

    raise HTTPException(status_code=404, detail="Data not available from any source")

# Fetch data from Stooq

def fetch_stooq(symbol):
    url = f"https://stooq.pl/q/d/l/?s={symbol}&i=d"
    response = requests.get(url)
    response.raise_for_status()
    df = pd.read_csv(StringIO(response.text))
    # Rename columns if needed
    df = df.rename(columns={
        'Data': 'Date',
        'Otwarcie': 'Open',
        'Najwyzszy': 'High',
        'Najnizszy': 'Low',
        'Zamkniecie': 'Close',
        'Wolumen': 'Volume'
    })
    return df

# Add technical indicators

def add_technical_indicators(df):
    import ta
    df = df.copy()
    from ta.trend import SMAIndicator, MACD
    from ta.momentum import RSIIndicator
    from ta.volatility import BollingerBands, AverageTrueRange
    from ta.trend import CCIIndicator
    # SMA
    df['SMA_14'] = SMAIndicator(df['Close'], window=14).sma_indicator()
    # RSI
    df['RSI_14'] = RSIIndicator(df['Close'], window=14).rsi()
    # MACD
    macd = MACD(df['Close'])
    df['MACD'] = macd.macd()
    df['Signal_Line'] = macd.macd_signal()
    df['MACD_Histogram'] = macd.macd_diff()
    # Bollinger Bands
    bb = BollingerBands(df['Close'], window=20)
    df['BB_High'] = bb.bollinger_hband()
    df['BB_Low'] = bb.bollinger_lband()
    # CCI
    df['CCI'] = CCIIndicator(df['High'], df['Low'], df['Close'], window=20).cci()
    # ATR
    df['ATR_14'] = AverageTrueRange(df['High'], df['Low'], df['Close'], window=14).average_true_range()
    return df

# Generate signal (simple rule-based)
def generate_signal(df, shares_owned=0):
    last = df.iloc[-1]
    rsi = last['RSI_14']
    macd = last['MACD']
    signal = "hold"
    if rsi > 70 and macd < 0 and shares_owned > 0:
        signal = "sell"
    elif rsi < 30 and macd > 0:
        signal = "buy"
    return signal

@router.get("/signals/{ticker}")
def get_signals(ticker: str, shares: int = 0):
    try:
        df = fetch_stooq(ticker)
        df = add_technical_indicators(df)
        signal = generate_signal(df, shares_owned=shares)
        return {"ticker": ticker, "signal": signal}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating signal: {e}")
