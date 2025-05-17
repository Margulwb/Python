import requests
import time
import os

def get_signal(symbol, shares):
    url = os.environ.get('ANALYZER_URL', 'http://analyzer:5000/signal')
    params = {'symbol': symbol, 'shares': shares}
    try:
        r = requests.get(url, params=params, timeout=10)
        r.raise_for_status()
        return r.json().get('signal')
    except Exception as e:
        print(f"Error fetching signal for {symbol}: {e}")
        return None

def notify_user(symbol, signal):
    print(f"[NOTIFY] {symbol}: {signal.upper()}")
    # Tu można dodać wysyłkę e-mail, SMS, push, itp.

if __name__ == "__main__":
    stocks = [
        {"symbol": "cdr", "shares": 2},
        {"symbol": "rbw", "shares": 0},
    ]
    last_signals = {s['symbol']: None for s in stocks}
    while True:
        for s in stocks:
            signal = get_signal(s['symbol'], s['shares'])
            if signal and signal != last_signals[s['symbol']]:
                notify_user(s['symbol'], signal)
                last_signals[s['symbol']] = signal
        time.sleep(60)  # sprawdzaj co minutę
