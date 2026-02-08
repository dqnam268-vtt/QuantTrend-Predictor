import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import numpy as np

class StockAI:
    def __init__(self, data):
        self.df = data

    def generate_signals(self):
        """Đánh giá dựa trên các chỉ số kỹ thuật (RSI, MA)"""
        last_row = self.df.iloc[-1]
        rsi = last_row['RSI']
        close = last_row['Close']
        ma20 = last_row['MA20']
        
        advice = ""
        score = 0 # Thang điểm từ -1 (Bán) đến 1 (Mua)

        # Logic đánh giá RSI
        if rsi > 70:
            advice += "RSI đang quá mua (Rất nóng). "
            score -= 0.5
        elif rsi < 30:
            advice += "RSI đang quá bán (Vùng giá rẻ). "
            score += 0.5
        
        # Logic đánh giá xu hướng MA20
        if close > ma20:
            advice += "Giá nằm trên MA20 (Xu hướng tăng). "
            score += 0.5
        else:
            advice += "Giá nằm dưới MA20 (Xu hướng giảm). "
            score -= 0.5

        return advice, score

    def predict_next_trend(self):
        """Sử dụng Machine Learning để dự đoán giá ngày mai Tăng hay Giảm"""
        df = self.df.copy()
        # Tạo nhãn: 1 nếu giá ngày mai cao hơn hôm nay, 0 nếu thấp hơn
        df['Target'] = (df['Close'].shift(-1) > df['Close']).astype(int)
        
        # Chọn các đặc trưng để học
        features = ['Close', 'RSI', 'MA20', 'Volume']
        X = df[features][:-1]
        y = df['Target'][:-1]

        # Huấn luyện mô hình Random Forest đơn giản
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X, y)

        # Dự đoán cho phiên tiếp theo
        last_features = df[features].iloc[-1:].values
        prediction = model.predict(last_features)
        
        return "Tăng" if prediction[0] == 1 else "Giảm"