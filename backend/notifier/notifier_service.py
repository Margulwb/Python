import requests
import time
import os
from flask import Flask, jsonify, request
from threading import Thread
from flask_cors import CORS
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Konfiguracja MongoDB
mongo_uri = os.environ.get("MONGO_URI", "mongodb://localhost:27017/")
mongo_client = MongoClient(mongo_uri)
db = mongo_client["stock_signals"]
signals_collection = db["signals"]

def get_signal(symbol, shares):
    url = os.environ.get('ANALYZER_URL', 'http://analyzer:5000/signal')
    params = {'symbol': symbol, 'shares': shares}
    try:
        print(f"Requesting signal for {symbol} with shares {shares}")
        r = requests.get(url, params=params, timeout=10)
        r.raise_for_status()
        print(f"Response from analyzer: {r.text}")
        return r.json().get('signal')
    except Exception as e:
        print(f"Error fetching signal for {symbol}: {e}")
        return None

def notify_user(stock, signal):
    print(f"[NOTIFY] {stock['symbol']} ({stock['name']}): {signal.upper()}")
    # Zapisz do MongoDB
    signals_collection.insert_one({
        "symbol": stock['symbol'],
        "name": stock['name'],
        "shares": stock['shares'],
        "signal": signal,
        "timestamp": datetime.utcnow()
    })

# Przechowywanie aktualnych sygnałów w pamięci
current_signals = {}

def get_stocks_from_db():
    stocks_cursor = db.stocks.find({}, {"_id": 0, "symbol": 1, "shares": 1, "name": 1})
    return list(stocks_cursor)

def background_task():
    global current_signals
    while True:
        stocks = get_stocks_from_db()
        for stock in stocks:
            signal = get_signal(stock['symbol'], stock['shares'])
            print(f"Fetching signal for {stock['symbol']}: {signal}")
            if signal and signal != current_signals.get(stock['symbol']):
                notify_user(stock, signal)
                current_signals[stock['symbol']] = signal
        time.sleep(60)


@app.route('/signals', methods=['GET'])
def get_signals():
    return jsonify(current_signals)

@app.route('/signals/history', methods=['GET'])
def get_signal_history():
    history = list(signals_collection.find({}, {"_id": 0}).sort("timestamp", -1).limit(100))
    return jsonify(history)

@app.route('/stocks', methods=['POST', 'GET'])
def stocks_handler():
    if request.method == 'POST':
        data = request.get_json()
        signal = get_signal(data['symbol'], data['shares'])  # Pobierz sygnał z analyzera
        profit = "0 PLN"  # Domyślna wartość zysku (można później obliczyć)
        db.stocks.insert_one({
            "symbol": data['symbol'],
            "name": data['name'],
            "shares": data['shares'],
            "signal": signal,
            "profit": profit
        })
        return jsonify({"message": "Stock added successfully", "signal": signal, "profit": profit}), 201

    elif request.method == 'GET':
        stocks_cursor = db.stocks.find({}, {"_id": 0})
        stocks = list(stocks_cursor)
        return jsonify(stocks), 200

@app.route('/stocks/<symbol>', methods=['DELETE'])
def delete_stock(symbol):
    result = db.stocks.delete_one({"symbol": symbol})
    if result.deleted_count > 0:
        return jsonify({"message": f"Stock with symbol {symbol} deleted successfully."}), 200
    else:
        return jsonify({"error": f"Stock with symbol {symbol} not found."}), 404

@app.route('/signals/reason/<symbol>', methods=['GET'])
def get_sell_reason(symbol):
    try:
        url = os.environ.get('ANALYZER_URL', 'http://analyzer:5000/reason')
        response = requests.get(f"{url}/{symbol}", timeout=10)
        response.raise_for_status()
        reason_data = response.json()

        # Debug logs
        print(f"Requesting reason from analyzer: {url}/{symbol}")
        print(f"Analyzer response status: {response.status_code}")
        print(f"Analyzer response body: {response.text}")

        # Save reason to MongoDB
        db.reasons.insert_one({
            "symbol": symbol,
            "reasons": reason_data.get("reasons", []),
            "timestamp": datetime.utcnow()
        })

        print(f"Saving reason to MongoDB for symbol: {symbol}")
        print(f"Reason data: {reason_data}")

        return jsonify(reason_data), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Failed to fetch reason from analyzer: {str(e)}"}), 500

if __name__ == "__main__":
    stocks = [
        {"symbol": "cdr", "name": "CD Projekt", "shares": 2},
        {"symbol": "rbw", "name": "Robimy Dobre Gry", "shares": 0},
    ]
    last_signals = {s['symbol']: None for s in stocks}
    thread = Thread(target=background_task)
    thread.daemon = True
    thread.start()

    app.run(host='0.0.0.0', port=5001)
