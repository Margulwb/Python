import requests
import pandas as pd
from io import StringIO

def fetch_stooq(symbol):
    print(f"Fetching data from Stooq for symbol: {symbol}")
    url = f"https://stooq.pl/q/d/l/?s={symbol}&i=d"
    response = requests.get(url)
    response.raise_for_status()
    print(f"Response status code: {response.status_code}")
    print(f"Response text: {response.text[:500]}...")  # Log first 500 characters of the response
    df = pd.read_csv(StringIO(response.text))
    df = df.rename(columns={
        'Data': 'Date',
        'Otwarcie': 'Open',
        'Najwyzszy': 'High',
        'Najnizszy': 'Low',
        'Zamkniecie': 'Close',
        'Wolumen': 'Volume'
    })
    return df
