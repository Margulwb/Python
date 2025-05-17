import pandas as pd
import time
from analyzer.src.data_fetcher import fetch_stooq
from analyzer.src.indicators import add_technical_indicators
from analyzer.src.signals import generate_signal, train_ml_model, ml_signal

def analyze_stock(symbol, shares_owned, label=None):
    df = fetch_stooq(symbol)
    df = add_technical_indicators(df)
    signal = generate_signal(df, shares_owned=shares_owned)
    return (label or symbol.upper(), signal)

if __name__ == "__main__":
    start = time.time()
    stocks = [
        {"symbol": "cdr", "shares": 2, "label": "CD Project Red (CDR)"},
        {"symbol": "rbw", "shares": 0, "label": "Rainbow Tours SA (RBW)"},
    ]
    results = []
    ml_models = {}
    for s in stocks:
        df = fetch_stooq(s["symbol"])
        df = add_technical_indicators(df)
        model, features = train_ml_model(df)
        ml_signal_result = ml_signal(df, model, features, shares_owned=s["shares"])
        results.append((s["label"], ml_signal_result))
    elapsed = time.time() - start
    for label, signal in results:
        print(f"{label} (AI): {signal.upper()}")
    print(f"Elapsed time: {elapsed:.3f} seconds")
