FROM python:3.11-slim
WORKDIR /app
RUN apt-get update && apt-get install -y curl gcc g++ && \
    apt-get clean && rm -rf /var/lib/apt/lists/*
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "analyzer_service.py"]
