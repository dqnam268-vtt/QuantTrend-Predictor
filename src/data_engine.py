import pandas as pd
from vnstock import VnstockV2 # Sửa lại để dùng bản V2 ổn định
from datetime import datetime, timedelta
import sys

class DataEngine:
    def __init__(self):
        self.tickers = ['HT1', 'VGI', 'VTP', 'FPT']
        self.stock = VnstockV2() # Khởi tạo đối tượng lấy dữ liệu

    def fetch_historical_data(self, symbol, days=365):
        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
        
        try:
            # Sửa cách gọi hàm thông qua đối tượng self.stock
            df = self.stock.stock_historical_data(symbol, start_date, end_date, resolution="1D", type="stock")
            
            if df is None or df.empty:
                return None
            
            df['time'] = pd.to_datetime(df['time'])
            df = df.sort_values('time')
            
            numeric_cols = ['open', 'high', 'low', 'close', 'volume']
            for col in numeric_cols:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce').astype('float32')
            
            return df.dropna(subset=['close'])
            
        except Exception as e:
            print(f"❌ Lỗi lấy dữ liệu {symbol}: {e}")
            return None