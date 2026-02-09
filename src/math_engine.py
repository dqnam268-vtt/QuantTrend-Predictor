import numpy as np
import pandas as pd
from scipy.fft import fft
from sklearn.linear_model import LinearRegression

class MathEngine:
    @staticmethod
    def calculate_fibonacci_levels(df):
        """Tính toán các mức thoái lui Fibonacci"""
        high_max = df['high'].max()
        low_min = df['low'].min()
        diff = high_max - low_min
        
        return {
            'Level_0': high_max,
            'Level_236': high_max - 0.236 * diff,
            'Level_382': high_max - 0.382 * diff,
            'Level_500': high_max - 0.5 * diff,
            'Level_618': high_max - 0.618 * diff,
            'Level_100': low_min
        }

    @staticmethod
    def monte_carlo_simulation(df, days=30, simulations=100):
        """Mô phỏng Monte Carlo để dự báo vùng giá rủi ro"""
        returns = df['close'].pct_change().dropna()
        last_price = df['close'].iloc[-1]
        
        results = []
        for _ in range(simulations):
            prices = [last_price]
            for _ in range(days):
                # Giả định giá biến động theo phân phối chuẩn dựa trên lịch sử
                price = prices[-1] * (1 + np.random.normal(returns.mean(), returns.std()))
                prices.append(price)
            results.append(prices)
            
        return np.array(results)

    @staticmethod
    def detect_cycles(data_series):
        """Sử dụng Fast Fourier Transform để tìm chu kỳ sóng"""
        n = len(data_series)
        close_fft = fft(data_series.values)
        # Chỉ lấy các thành phần tần số chính
        return np.abs(close_fft[:n//2])