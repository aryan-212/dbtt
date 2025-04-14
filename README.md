# Multi-source Financial Data Analytics Platform

A real-time financial data analytics platform that collects data from multiple sources (Binance and Finnhub), processes it through Kafka, and provides analytics via a FastAPI backend.

## Features

- Real-time data collection from:
  - Binance WebSocket (Crypto data)
  - Finnhub WebSocket (Stock data)
- Data processing with Apache Kafka
- Analytics:
  - Moving averages
  - OHLC (Open, High, Low, Close) calculations
  - Volume spike detection
- PostgreSQL storage for raw and processed data
- FastAPI backend with REST and WebSocket endpoints

## Prerequisites

- Python 3.8+
- Apache Kafka
- PostgreSQL
- Finnhub API Key (get it from https://finnhub.io)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd <repository-name>
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
- Copy `.env.example` to `.env`
- Fill in your configuration values:
  - Kafka bootstrap servers
  - PostgreSQL credentials
  - Finnhub API key

## Running the Application

1. Start Kafka and PostgreSQL:
```bash
# Make sure Kafka and PostgreSQL are running on your system
```

2. Start the Binance producer:
```bash
python -m src.producers.binance
```

3. Start the Finnhub producer:
```bash
python -m src.producers.finnhub
```

4. Start the Kafka consumer:
```bash
python -m src.consumers.market_data_consumer
```

5. Start the FastAPI backend:
```bash
uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000
```

## API Endpoints

### REST Endpoints

- `GET /latest-data?symbol=BTCUSDT&limit=100`
  - Get latest market data for a symbol
  - Optional query parameters:
    - `limit`: Number of records to return (default: 100, max: 1000)

- `GET /ohlc?symbol=BTCUSDT&timeframe=1min`
  - Get OHLC (candlestick) data
  - Optional query parameters:
    - `timeframe`: Time period (e.g., "1min", "5min", "1hour")
    - `start_time`: ISO format datetime
    - `end_time`: ISO format datetime
    - `limit`: Number of candles to return

- `GET /alerts?symbol=BTCUSDT&alert_type=VOLUME_SPIKE`
  - Get market alerts
  - Optional query parameters:
    - `symbol`: Filter by symbol
    - `alert_type`: Filter by alert type
    - `limit`: Number of alerts to return

### WebSocket Endpoint

- `ws://localhost:8000/ws/market-data/{symbol}`
  - Real-time market data updates
  - Replace `{symbol}` with the desired symbol (e.g., "BTCUSDT", "AAPL")

## Project Structure

```
.
├── requirements.txt
├── .env
└── src/
    ├── producers/
    │   ├── binance.py
    │   └── finnhub.py
    ├── consumers/
    │   └── market_data_consumer.py
    ├── models/
    │   ├── base.py
    │   └── market_data.py
    ├── analytics/
    │   └── processor.py
    └── api/
        └── main.py
```

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 