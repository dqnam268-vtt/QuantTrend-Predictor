import pandas as pd
from vnstock import stock_historical_data
from datetime import datetime, timedelta

class DataEngine:
    def __init__(self):
        self.tickers = ['FPT', 'HT1', 'HPG', 'VIC']

    def fetch_historical_data(self, symbol, days=365):
        """Lấy dữ liệu lịch sử và làm sạch"""
        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
        
        try:
            df = stock_historical_data(symbol, start_date, end_date, resolution="1D", type="stock")
            if df.empty:
                return None
            
            # Chuẩn hóa dữ liệu
            df['time'] = pd.to_datetime(df['time'])
            df = df.sort_values('time')
            # Đảm bảo các cột số liệu là float
            cols = ['open', 'high', 'low', 'close', 'volume']
            df[cols] = df[cols].astype(float)
            return df
        except Exception as e:
            print(f"Lỗi khi lấy dữ liệu {symbol}: {e}")
            return None

    def get_realtime_quote(self, symbol):
        """Lấy giá cập nhật nhất (giả lập hoặc từ bảng giá)"""
        # Lưu ý: vnstock cung cấp các hàm realtime tùy thuộc vào nguồn API khả dụng
        return self.fetch_historical_data(symbol, days=5).iloc[-1:]