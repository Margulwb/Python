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

@app.route('/reason/<symbol>', methods=['GET'])
def get_reason(symbol):
    try:
        df = fetch_stooq(symbol)
        df = add_technical_indicators(df)

        reasons = []
        last_row = df.iloc[-1]

        # RSI logic
        if last_row['RSI_14'] > 70:
            reasons.append(f"RSI wskazuje na wykupienie akcji (RSI: {last_row['RSI_14']:.2f}).")
        elif last_row['RSI_14'] < 30:
            reasons.append(f"RSI wskazuje na wyprzedanie akcji (RSI: {last_row['RSI_14']:.2f}).")

        # MACD logic
        if last_row['MACD'] < last_row['Signal_Line']:
            reasons.append("MACD wskazuje na niedźwiedzi crossover.")
        elif last_row['MACD'] > last_row['Signal_Line']:
            reasons.append("MACD wskazuje na byczy crossover.")

        # Bollinger Bands logic
        if last_row['Close'] >= last_row['BB_High']:
            reasons.append("Cena znajduje się blisko górnej wstęgi Bollingera, co wskazuje na wykupienie.")
        elif last_row['Close'] <= last_row['BB_Low']:
            reasons.append("Cena znajduje się blisko dolnej wstęgi Bollingera, co wskazuje na wyprzedanie.")

        # ATR logic
        if last_row['ATR_14'] > df['ATR_14'].mean():
            reasons.append("Wykryto wysoką zmienność (ATR powyżej średniej).")

        # CCI logic
        if last_row['CCI'] > 100:
            reasons.append("CCI wskazuje na wykupienie akcji.")
        elif last_row['CCI'] < -100:
            reasons.append("CCI wskazuje na wyprzedanie akcji.")

        # Combine reasons
        if not reasons:
            reasons.append("Nie wykryto istotnych wskaźników.")

        return jsonify({'symbol': symbol.upper(), 'reasons': reasons}), 200
    except Exception as e:
        return jsonify({'error': f'Failed to generate reasons: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
