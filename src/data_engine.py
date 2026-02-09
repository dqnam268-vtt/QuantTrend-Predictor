import pandas as pd
from vnstock import stock_historical_data
from datetime import datetime, timedelta
import sys

# Tối ưu: Ngăn chặn vnstock gọi các thư viện giao diện khi chạy trên server
class DataEngine:
    def __init__(self):
        # Tập trung vào các mã bạn quan tâm
        self.tickers = ['HT1', 'VGI', 'VTP', 'FPT']

    def fetch_historical_data(self, symbol, days=365):
        """Lấy dữ liệu với cơ chế xử lý lỗi ngoại lệ chặt chẽ"""
        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
        
        try:
            # Tối ưu: Sử dụng resolution="1D" để giảm dung lượng tải
            df = stock_historical_data(symbol, start_date, end_date, resolution="1D", type="stock")
            
            if df is None or df.empty:
                print(f"⚠️ Cảnh báo: Không có dữ liệu cho mã {symbol}")
                return None
            
            # Tối ưu: Ép kiểu dữ liệu ngay lập tức để tiết kiệm RAM
            df['time'] = pd.to_datetime(df['time'])
            df = df.sort_values('time')
            
            numeric_cols = ['open', 'high', 'low', 'close', 'volume']
            for col in numeric_cols:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce').astype('float32')
            
            # Loại bỏ các dòng lỗi (NaN)
            df = df.dropna(subset=['close'])
            
            return df
            
        except Exception as e:
            print(f"❌ Lỗi hệ thống khi lấy dữ liệu {symbol}: {e}")
            return None

    def get_batch_data(self):
        """Tối ưu: Lấy dữ liệu hàng loạt cho danh mục"""
        results = {}
        for ticker in self.tickers:
            data = self.fetch_historical_data(ticker)
            if data is not None:
                results[ticker] = data
        return results

if __name__ == "__main__":
    # Test nhanh khi chạy GitHub Actions
    engine = DataEngine()
    print("🚀 Đang kiểm tra kết nối dữ liệu...")
    test_data = engine.fetch_historical_data("HT1", days=10)
    if test_data is not None:
        print(f"✅ Kết nối thành công. Giá đóng cửa gần nhất của HT1: {test_data['close'].iloc[-1]}")
        sys.exit(0) # Thoát với mã thành công
    else:
        print("❌ Kết nối thất bại.")
        sys.exit(1) # Thoát với mã lỗi để GitHub Actions báo đỏ