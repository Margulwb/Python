import sys
import os
from src.data_fetcher import fetch_stooq
from src.indicators import add_technical_indicators
from src.signals import train_ml_model, ml_signal

from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/signal', methods=['GET'])
def get_signal():
    symbol = request.args.get('symbol')
    shares = int(request.args.get('shares', 0))
    if not symbol:
        return jsonify({'error': 'Missing symbol'}), 400
    df = fetch_stooq(symbol)
    df = add_technical_indicators(df)
    model, features = train_ml_model(df)
    signal = ml_signal(df, model, features, shares_owned=shares)
    return jsonify({
        'symbol': symbol.upper(),
        'shares': shares,
        'signal': signal
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
