import pandas as pd
from vnstock import stock_historical_data
from datetime import datetime, timedelta

class DataEngine:
    def fetch_data(self, symbol, days=365):
        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
        try:
            # Lấy dữ liệu từ nguồn tin cậy nhất cho mã VN
            df = stock_historical_data(symbol, start_date, end_date, resolution="1D", type="stock")
            if df.empty: return None
            df['time'] = pd.to_datetime(df['time'])
            df.set_index('time', inplace=True)
            cols = ['open', 'high', 'low', 'close', 'volume']
            df[cols] = df[cols].astype(float)
            return df
        except:
            return None