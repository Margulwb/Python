import requests
import pandas as pd
from io import StringIO

def fetch_stooq(symbol):
    url = f"https://stooq.pl/q/d/l/?s={symbol}&i=d"
    response = requests.get(url)
    response.raise_for_status()
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
