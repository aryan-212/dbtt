import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict, Any

class MarketDataProcessor:
    def __init__(self, window_size: int = 20):
        self.window_size = window_size
        self.data_buffer: Dict[str, List[Dict[str, Any]]] = {}  # Buffer for each symbol
        self.last_ohlc: Dict[str, pd.DataFrame] = {}  # Last OHLC for each symbol

    def add_data(self, message: Dict[str, Any]) -> None:
        """Add new market data to the buffer."""
        symbol = message['symbol']
        if symbol not in self.data_buffer:
            self.data_buffer[symbol] = []
        self.data_buffer[symbol].append(message)

    def calculate_moving_average(self, symbol: str) -> float:
        """Calculate simple moving average for the last window_size prices."""
        if symbol not in self.data_buffer or len(self.data_buffer[symbol]) < self.window_size:
            return None
        
        prices = [float(data['price']) for data in self.data_buffer[symbol][-self.window_size:]]
        return sum(prices) / len(prices)

    def calculate_ohlc(self, symbol: str, timeframe_minutes: int = 1) -> Dict[str, Any]:
        """Calculate OHLC for the given symbol and timeframe."""
        if symbol not in self.data_buffer or not self.data_buffer[symbol]:
            return None

        # Convert data to DataFrame
        df = pd.DataFrame(self.data_buffer[symbol])
        df['event_time'] = pd.to_datetime(df['event_time'])
        
        # Resample to 1-minute OHLC
        ohlc = df.set_index('event_time').resample(f'{timeframe_minutes}T').agg({
            'price': ['first', 'max', 'min', 'last'],
            'volume': 'sum'
        }).dropna()

        if ohlc.empty:
            return None

        # Format the latest OHLC data
        latest = ohlc.iloc[-1]
        return {
            'symbol': symbol,
            'timestamp': ohlc.index[-1].isoformat(),
            'open': latest['price']['first'],
            'high': latest['price']['max'],
            'low': latest['price']['min'],
            'close': latest['price']['last'],
            'volume': latest['volume']['sum']
        }

    def detect_volume_spike(self, symbol: str, threshold_multiplier: float = 3.0) -> Dict[str, Any]:
        """Detect volume spikes using rolling mean comparison."""
        if symbol not in self.data_buffer or len(self.data_buffer[symbol]) < self.window_size:
            return None

        df = pd.DataFrame(self.data_buffer[symbol])
        df['event_time'] = pd.to_datetime(df['event_time'])
        
        # Calculate rolling mean volume
        rolling_mean = df['volume'].rolling(window=self.window_size).mean()
        current_volume = df['volume'].iloc[-1]
        
        if current_volume > (rolling_mean.iloc[-1] * threshold_multiplier):
            return {
                'symbol': symbol,
                'alert_type': 'VOLUME_SPIKE',
                'message': f'Volume spike detected for {symbol}',
                'timestamp': df['event_time'].iloc[-1].isoformat(),
                'value': float(current_volume)
            }
        return None

    def process_batch(self, symbol: str) -> Dict[str, Any]:
        """Process a batch of data and return analytics results."""
        results = {
            'moving_average': self.calculate_moving_average(symbol),
            'ohlc': self.calculate_ohlc(symbol),
            'volume_alert': self.detect_volume_spike(symbol)
        }
        
        # Clear processed data while keeping the last window_size elements
        if symbol in self.data_buffer and len(self.data_buffer[symbol]) > self.window_size * 2:
            self.data_buffer[symbol] = self.data_buffer[symbol][-self.window_size:]
            
        return results 