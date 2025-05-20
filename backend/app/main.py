from fastapi import FastAPI
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import atexit
import time
from app.routers import stocks

app = FastAPI()

# MongoDB setup
max_retries = 15
retry_delay = 10  # seconds
for attempt in range(max_retries):
    try:
        mongo_client = MongoClient("mongodb://mongo:27017/", serverSelectionTimeoutMS=2000)
        # Trigger server selection to check connection
        mongo_client.admin.command('ping')
        break
    except ServerSelectionTimeoutError as e:
        print(f"[MongoDB] Connection failed (attempt {attempt+1}/{max_retries}): {e}")
        time.sleep(retry_delay)
else:
    raise RuntimeError("[MongoDB] Could not connect to MongoDB after multiple attempts.")

db = mongo_client["stock_data"]
stocks_collection = db["stocks"]

# Scheduler setup
scheduler = BackgroundScheduler()

# Define the scheduled task
def scheduled_task():
    tickers = stocks_collection.distinct("ticker")
    for ticker in tickers:
        print(f"Checking data and generating signal for {ticker}")
        # Placeholder for data checking and signal generation logic
        pass

# Add the task to the scheduler
scheduler.add_job(scheduled_task, IntervalTrigger(minutes=5))
scheduler.start()

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())

app.include_router(stocks.router)

@app.get("/stocks")
def read_stocks():
    return {"message": "This is a placeholder for the /stocks endpoint."}
