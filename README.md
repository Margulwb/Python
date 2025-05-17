# 📈 AI Stock Signal Notifier – CD Projekt Red (CDR)

An AI-powered application that analyzes stock data and informs you when to **buy**, **sell**, or **hold** shares of **CD Projekt Red** (ticker: `CDR` on the Warsaw Stock Exchange).

---

## 🔍 Project Goal

To build a tool that automatically:
- Fetches stock data for CDR,
- Analyzes it using technical analysis and/or AI,
- Generates trading signals (buy/sell/hold),
- Notifies the user about recommended actions.

---

## 🧠 Technologies Used

### Backend / ML
- Python 3.x
- `pandas`, `numpy` – data processing
- `scikit-learn`, `xgboost`, `prophet` – predictive models
- `TA-Lib`, `bt`, `backtrader` – technical analysis
- `Flask` – REST API for communication
- `smtplib`, `requests` – sending notifications

### Frontend
- **React** – interactive dashboard (connects with Flask API via HTTP)

### Mobile
- **Flutter** – mobile app (Android / iOS) to display signals and receive alerts

### Notifications
- Email
- Push (e.g., Pushover, Telegram, SMS via Twilio)

---

## 🔗 Data Sources

Stock market data for CDR can be retrieved from:
- [Stooq.pl](https://stooq.pl) (free data, scraping possible)
- Yahoo Finance API *(limited GPW support)*
- Paid APIs: Refinitiv, GPW Benchmark, Alpha Vantage, Quandl

---

## 🚀 MVP – Minimum Viable Product

1. Python script:
    - Fetches daily stock data for `CDR`,
    - Calculates basic indicators (e.g., RSI, SMA),
    - Generates a trading signal (buy / sell),
    - Sends an email notification.

2. Once validated:
    - Extend with an ML/AI model,
    - Add a React dashboard and Flutter mobile client.

---

## 🧠 AI/ML – Possible Approaches

### 1. Supervised Learning
Train a model on historical stock data:
- Features: RSI, MACD, SMA, volume, etc.
- Target: price movement (up/down)

### 2. Reinforcement Learning
An agent learns to maximize profits by deciding when to buy/sell.

### 3. Sentiment Analysis *(optional)*
Analyze news and social media sentiment (e.g., Twitter, Reddit) about CD Projekt Red.

---

## 🧱 Tech Stack

| Layer     | Technology            |
|-----------|------------------------|
| Backend   | Python 3.11 + Flask    |
| AI        | Scikit-learn / XGBoost |
| Tech Analysis | TA-Lib / Backtrader |
| Frontend  | React                  |
| Mobile    | Flutter                |
| Alerts    | SMTPLib / Telegram API |

---

## 🗓 Future Enhancements

- Flutter-based mobile app with push notifications (e.g., Firebase)
- Web dashboard with visual charts (React + Chart.js / Recharts)
- Strategy backtesting using `backtrader`
- Support for multiple stock tickers
- Dockerized deployment

---

## 📬 Author

**Maciej Gurgul**  
DevOps Engineer
Applied Computer Science student at WSEI

---

> ⚠️ Disclaimer: This project is for educational purposes only. It does not constitute financial or investment advice.


# 📈 AI Stock Signal Notifier – CD Projekt Red (CDR)

Aplikacja wspierana przez sztuczną inteligencję, która analizuje dane giełdowe i informuje, kiedy warto **kupić**, **sprzedać** lub **trzymać** akcje **CD Projekt Red** (ticker: `CDR` na GPW).

---

## 🔍 Cel projektu

Zbudować narzędzie, które automatycznie:
- Pobiera dane giełdowe dla CDR,
- Analizuje dane z wykorzystaniem analizy technicznej i/lub AI,
- Generuje sygnały inwestycyjne (kup/sprzedaj/trzymaj),
- Powiadamia użytkownika o rekomendowanych działaniach.

- pokazuje zysk

---

## 🧠 Wykorzystane technologie

### Backend / ML
- Python 3.x
- `pandas`, `numpy` – przetwarzanie danych
- `scikit-learn`, `xgboost`, `prophet` – modele predykcyjne
- `TA-Lib`, `bt`, `backtrader` – analiza techniczna
- `smtplib`, `requests` – powiadomienia

### Frontend (opcjonalny)
- React / Flask (Web)
- React Native / Flutter (Mobile)

### Powiadomienia
- E-mail
- Push (np. Pushover, Telegram, SMS przez Twilio)

---

## 🔗 Dane wejściowe

Źródła danych giełdowych:
- [Stooq.pl](https://stooq.pl) (dane GPW, możliwe scrapowanie)
- Yahoo Finance API *(ograniczone wsparcie dla GPW)*
- Płatne API: Refinitiv, GPW Benchmark, Alpha Vantage, Quandl

---

## 🚀 MVP – Minimalna wersja produktu

1. Skrypt w Pythonie:
    - Pobiera dane dla `CDR` raz dziennie,
    - Liczy wskaźniki techniczne (np. RSI, SMA),
    - Generuje sygnał (kup / sprzedaj),
    - Wysyła powiadomienie e-mail.

2. Po walidacji skuteczności:
    - Rozbudowa o model ML/AI,
    - Dodanie dashboardu / UI.

---

## 🧠 AI/ML – możliwe podejścia

### 1. Supervised Learning
Uczenie na danych historycznych:
- Cechy: RSI, MACD, SMA, wolumen, itp.
- Cel: przewidzenie zmiany ceny (+/-)

### 2. Reinforcement Learning
Agent podejmuje decyzje inwestycyjne z uwagi na maksymalizację zysków.

### 3. Sentiment Analysis *(opcjonalnie)*
Analiza nastrojów z newsów i social mediów (np. Twitter, Reddit).

---

## 🧱 Stack technologiczny (propozycja)

| Warstwa | Technologia |
|--------|-------------|
| Backend | Python 3.11 |
| AI | Scikit-learn / XGBoost |
| Analiza techniczna | TA-Lib / Backtrader |
| UI (opcjonalnie) | React / Flask |
| Powiadomienia | SMTPLib / Telegram API |

---

## 🗓 Przyszłe usprawnienia

- Wersja mobilna z powiadomieniami push
- Web dashboard z wykresami (Plotly, Dash)
- Backtest strategii z użyciem `backtrader`
- Obsługa wielu spółek giełdowych
- Wersja Dockerowa

---

## 📬 Autor

**Maciej Gurgul**  
DevOps Engineer
Student Informatyki Stosowanej na WSEI

---

> ⚠️ Disclaimer: Projekt ma charakter edukacyjny. Nie stanowi porady inwestycyjnej.
