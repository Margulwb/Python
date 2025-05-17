from sklearn.ensemble import RandomForestClassifier
import numpy as np

def train_ml_model(df):
    df = df.dropna().copy()
    features = [
        'SMA_14', 'RSI_14', 'MACD', 'BB_High', 'BB_Low', 'CCI', 'EMA_14', 'WMA_14',
        'WILLR_14', 'STOCH_K', 'STOCH_D', 'ATR_14', 'OBV', 'CMF', 'ROC', 'ICHIMOKU_A',
        'ICHIMOKU_B', 'DONCHIAN_H', 'DONCHIAN_L', 'MFI', 'EOM', 'FI'
    ]
    X = df[features].values
    y = (df['Close'].shift(-1) > df['Close']).astype(int)[:-1]
    X = X[:-1]
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)
    return model, features

def ml_signal(df, model, features, shares_owned=0):
    last = df.dropna().iloc[-1]
    X_last = last[features].values.reshape(1, -1)
    pred = model.predict(X_last)[0]
    if pred == 1 and shares_owned == 0:
        return 'buy'
    elif pred == 0 and shares_owned > 0:
        return 'sell'
    else:
        return 'hold'

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
