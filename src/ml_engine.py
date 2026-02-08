import numpy as np
import pandas as pd
from sklearn.preprocessing import RobustScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from ta.momentum import RSIIndicator
from ta.trend import SMAIndicator

class MLEngine:
    def __init__(self):
        self.scaler = RobustScaler()
        
    def add_indicators(self, df):
        df['RSI'] = RSIIndicator(close=df['close']).rsi()
        df['MA20'] = SMAIndicator(close=df['close'], window=20).sma_indicator()
        df['MA50'] = SMAIndicator(close=df['close'], window=50).sma_indicator()
        return df.fillna(method='bfill')

    def predict_trend(self, df):
        # Mô hình học nhanh xu hướng ngắn hạn
        data = df[['close', 'volume', 'RSI']].tail(60).values
        scaled_data = self.scaler.fit_transform(data)
        
        # Giả lập mô hình dự báo nhanh (có thể thay bằng model.load nếu đã train)
        last_price = df['close'].iloc[-1]
        rsi = df['RSI'].iloc[-1]
        
        # Logic AI đánh giá mạnh
        strength = "Tích cực" if (rsi > 45 and rsi < 70) else "Thận trọng"
        if rsi > 75: strength = "Quá nóng (Rủi ro)"
        if rsi < 30: strength = "Vùng đáy (Cơ hội)"
        
        return strength, last_price * 1.02 # Dự báo mục tiêu ngắn hạn +2%