import numpy as np
from sklearn.linear_model import LinearRegression

class MathEngine:
    @staticmethod
    def calculate_ema(data, window=20):
        """Exponential Moving Average - Ưu tiên dữ liệu gần hiện tại hơn"""
        return data.ewm(span=window, adjust=False).mean()

    @staticmethod
    def linear_trendline(data_series):
        """
        Tính đường xu thế tuyến tính: y = ax + b
        Trả về: mảng giá trị xu thế, hệ số góc (slope)
        """
        y = data_series.values.reshape(-1, 1)
        x = np.arange(len(y)).reshape(-1, 1)
        
        model = LinearRegression()
        model.fit(x, y)
        
        trend = model.predict(x)
        slope = model.coef_[0][0]
        
        return trend.flatten(), slope

    @staticmethod
    def calculate_volatility(data_series, window=20):
        """Tính độ lệch chuẩn để xác định vùng biến động (Bollinger-like)"""
        return data_series.rolling(window=window).std()