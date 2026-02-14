import subprocess
import sys
import os

# --- CÀI ĐẶT CƯỠNG BỨC (FORCE INSTALL) ---
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

try:
    from vnstock import stock_historical_data
except ImportError:
    install('vnstock')
    install('beautifulsoup4')
    install('ipython')

# --- ĐIỀU CHỈNH ĐƯỜNG DẪN HỆ THỐNG ---
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Bây giờ mới gọi các Engine của thầy
from data_engine import DataEngine
from ml_engine import MLEngine
from math_engine import MathEngine

import streamlit as st
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

# Bây giờ thầy mới gọi các engine như cũ, hệ thống sẽ không còn báo lỗi nữa
from data_engine import DataEngine
from ml_engine import MLEngine
from math_engine import MathEngine

# --- SỬA LỖI ĐƯỜNG DẪN (PATH FIX) ---
# Dòng này giúp Streamlit nhận diện được các file engine nằm cùng thư mục src
sys.path.append(os.path.dirname(__file__))

# Import các công cụ toán học và AI từ các file thầy đã viết
from data_engine import DataEngine
from ml_engine import MLEngine
from math_engine import MathEngine

st.set_page_config(page_title="Hệ thống Dự báo AI - Thầy Nam", layout="wide")

# --- GIAO DIỆN SIDEBAR ---
st.sidebar.title("💎 Cấu hình Hệ thống")
symbol = st.sidebar.selectbox("Chọn mã theo dõi:", ["HT1", "VGI", "VTP", "FPT"])
days_to_load = st.sidebar.slider("Dữ liệu lịch sử (ngày):", 100, 730, 365)

st.title(f"📊 Phân tích & Dự báo AI: {symbol}")

# --- KHỞI TẠO ENGINE ---
db = DataEngine()
ai = MLEngine()

# Sử dụng đúng tên hàm fetch_historical_data từ file data_engine.py của thầy
data = db.fetch_historical_data(symbol, days=days_to_load)

if data is not None:
    # Bổ sung các chỉ số kỹ thuật (RSI, MA)
    data = ai.add_indicators(data)
    
    # Dự báo xu hướng và mục tiêu giá
    trend, target = ai.predict_trend(data)
    
    # --- DASHBOARD CHỈ SỐ NHANH ---
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Giá hiện tại", f"{data['close'].iloc[-1]:,.0f}đ")
    with c2:
        st.metric("Trạng thái AI", trend)
    with c3:
        st.metric("Mục tiêu dự kiến (T+)", f"{target:,.0f}đ")

    # --- TABS PHÂN TÍCH ---
    tab1, tab2, tab3 = st.tabs(["📉 Biểu đồ AI", "🎲 Xác suất Monte Carlo", "📐 Vùng giá Fibonacci"])

    with tab1:
        fig = go.Figure()
        fig.add_trace(go.Candlestick(x=data['time'], open=data['open'], high=data['high'], 
                                     low=data['low'], close=data['close'], name='Nến giá'))
        fig.add_trace(go.Scatter(x=data['time'], y=data['MA20'], name='MA20', line=dict(color='orange')))
        fig.add_trace(go.Scatter(x=data['time'], y=data['MA50'], name='MA50', line=dict(color='blue')))
        fig.update_layout(height=600, template='plotly_dark', xaxis_rangeslider_visible=False)
        st.plotly_chart(fig, use_container_width=True)
        
        st.subheader("🤖 Nhận định từ Trí tuệ nhân tạo")
        st.info(f"Dựa trên dữ liệu lịch sử, mã **{symbol}** đang có xu hướng **{trend}**. RSI hiện tại là {data['RSI'].iloc[-1]:.2f}.")

    with tab2:
        st.subheader("🎲 Mô phỏng xác suất Monte Carlo (30 ngày tới)")
        # Gọi hàm mô phỏng từ math_engine.py
        sims = MathEngine.monte_carlo_simulation(data)
        fig_mc = go.Figure()
        for i in range(len(sims)):
            fig_mc.add_trace(go.Scatter(y=sims[i], mode='lines', line=dict(width=1), showlegend=False, opacity=0.3))
        fig_mc.update_layout(template='plotly_dark', title="100 Kịch bản biến động giá có thể xảy ra")
        st.plotly_chart(fig_mc, use_container_width=True)

    with tab3:
        st.subheader("📐 Các ngưỡng hỗ trợ & Kháng cự Fibonacci")
        # Tính toán các mức giá quan trọng
        fib = MathEngine.calculate_fibonacci_levels(data)
        col_fib1, col_fib2 = st.columns(2)
        for i, (level, value) in enumerate(fib.items()):
            if i % 2 == 0:
                col_fib1.write(f"**{level}:** {value:,.0f}đ")
            else:
                col_fib2.write(f"**{level}:** {value:,.0f}đ")
        st.progress(0.618)
else:
    st.error(f"❌ Không thể tải dữ liệu cho mã {symbol}. Vui lòng kiểm tra lại kết nối mạng hoặc phiên giao dịch.")