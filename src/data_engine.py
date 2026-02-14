import pandas as pd
from vnstock import VnstockV2 # Dùng bản V2 để ổn định
from datetime import datetime, timedelta

class DataEngine:
    def __init__(self):
        self.tickers = ['HT1', 'VGI', 'VTP', 'FPT']
        # Khởi tạo đối tượng lấy dữ liệu
        self.stock = VnstockV2()

    def fetch_historical_data(self, symbol, days=365):
        """Lấy dữ liệu lịch sử chuẩn hóa cho App"""
        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
        
        try:
            # Gọi hàm thông qua đối tượng VnstockV2
            df = self.stock.stock_historical_data(symbol, start_date, end_date, resolution="1D", type="stock")
            
            if df is None or df.empty:
                return None
            
            # Tiền xử lý dữ liệu
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