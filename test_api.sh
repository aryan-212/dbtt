#!/bin/bash

echo "Testing Market Data API Endpoints"
echo "--------------------------------"

echo -e "\n1. Basic Market Data Request (should return error without symbol):"
curl -s -X GET "http://localhost:8000/api/v1/market-data" | jq

echo -e "\n2. Market Data with Symbol Filter (BTCUSDT):"
curl -s -X GET "http://localhost:8000/api/v1/market-data?symbol=BTCUSDT" | jq

echo -e "\n3. Market Data with Symbol Filter (AAPL):"
curl -s -X GET "http://localhost:8000/api/v1/market-data?symbol=AAPL" | jq

echo -e "\n4. Market Data with Timeframe (1m):"
curl -s -X GET "http://localhost:8000/api/v1/market-data?symbol=BTCUSDT&timeframe=1m" | jq

echo -e "\n5. Market Data with Timeframe (5m):"
curl -s -X GET "http://localhost:8000/api/v1/market-data?symbol=BTCUSDT&timeframe=5m" | jq

echo -e "\n6. Market Data with Limit:"
curl -s -X GET "http://localhost:8000/api/v1/market-data?symbol=BTCUSDT&limit=5" | jq

echo -e "\n7. Market Data with Time Range:"
curl -s -X GET "http://localhost:8000/api/v1/market-data?symbol=BTCUSDT&start_time=2025-04-14T15:50:00Z&end_time=2025-04-14T16:00:00Z" | jq

echo -e "\n8. Market Data with All Parameters:"
curl -s -X GET "http://localhost:8000/api/v1/market-data?symbol=BTCUSDT&timeframe=1m&start_time=2025-04-14T15:50:00Z&end_time=2025-04-14T16:00:00Z&limit=5" | jq

echo -e "\n9. Invalid Symbol Test:"
curl -s -X GET "http://localhost:8000/api/v1/market-data?symbol=INVALID" | jq

echo -e "\n10. Invalid Timeframe Test:"
curl -s -X GET "http://localhost:8000/api/v1/market-data?symbol=BTCUSDT&timeframe=invalid" | jq

echo -e "\n11. Invalid Time Range Test:"
curl -s -X GET "http://localhost:8000/api/v1/market-data?symbol=BTCUSDT&start_time=invalid&end_time=invalid" | jq

echo -e "\n12. Available Symbols:"
curl -s -X GET "http://localhost:8000/api/v1/symbols" | jq

echo -e "\n13. Available Timeframes:"
curl -s -X GET "http://localhost:8000/api/v1/timeframes" | jq

echo -e "\n14. Legacy Latest Data:"
curl -s -X GET "http://localhost:8000/latest-data?symbol=BTCUSDT&limit=10" | jq

echo -e "\n15. Legacy OHLC Data:"
curl -s -X GET "http://localhost:8000/ohlc?symbol=BTCUSDT&timeframe=1min&limit=10" | jq

echo -e "\n16. Legacy Alerts:"
curl -s -X GET "http://localhost:8000/alerts?symbol=BTCUSDT&limit=10" | jq 