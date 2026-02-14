import streamlit as st
import plotly.graph_objects as go
from src.data_engine import DataEngine
from ml_engine import MLEngine
from math_engine import MathEngine


st.set_page_config(page_title="AI QuantTrend Predictor", layout="wide")

# Giao diện Sidebar
st.sidebar.title("💎 Cấu hình Hệ thống")
symbol = st.sidebar.selectbox("Chọn mã theo dõi:", ["HT1", "VGI", "VTP", "FPT"])
days = st.sidebar.slider("Dữ liệu phân tích (ngày):", 100, 730, 365)

st.title(f"📊 Phân tích & Dự báo AI: {symbol}")

# Khởi tạo Engine
db = DataEngine()
ai = MLEngine()

data = db.fetch_data(symbol, days)

if data is not None:
    data = ai.add_indicators(data)
    trend, target = ai.predict_trend(data)
    
    # Dashboard chỉ số nhanh
    c1, c2, c3 = st.columns(3)
    c1.metric("Giá hiện tại", f"{data['close'].iloc[-1]:,.0f}đ")
    c2.metric("Trạng thái AI", trend)
    c3.metric("Mục tiêu dự kiến", f"{target:,.0f}đ")

    # Biểu đồ kỹ thuật chuyên sâu
    fig = go.Figure()
    fig.add_trace(go.Candlestick(x=data.index, open=data['open'], high=data['high'], 
                                 low=data['low'], close=data['close'], name='Nến giá'))
    fig.add_trace(go.Scatter(x=data.index, y=data['MA20'], name='MA20', line=dict(color='orange')))
    fig.add_trace(go.Scatter(x=data.index, y=data['MA50'], name='MA50', line=dict(color='blue')))
    
    fig.update_layout(height=600, template='plotly_dark', xaxis_rangeslider_visible=False)
    st.plotly_chart(fig, use_container_width=True)

    # Đánh giá chi tiết từ AI
    st.subheader("🤖 Chiến lược từ Trí tuệ nhân tạo")
    with st.expander("Xem chi tiết đánh giá"):
        st.write(f"- **Xu hướng:** {symbol} đang ở trạng thái {trend}.")
        st.write(f"- **Chỉ số RSI:** {data['RSI'].iloc[-1]:.2f} (Dưới 30: Mua, Trên 70: Bán).")
        st.write("- **Khuyến nghị:** Dựa trên phân tích dòng tiền và MA, hệ thống đề xuất tỷ trọng an toàn là 30-50% tiền mặt.")
else:
    st.error("Không thể kết nối dữ liệu. Vui lòng kiểm tra lại mã cổ phiếu.")
# ... (Phần lấy dữ liệu cũ)

tab1, tab2, tab3 = st.tabs(["Biểu đồ AI", "Xác suất Monte Carlo", "Vùng giá Fibonacci"])

with tab1:
    # Biểu đồ nến cũ đã làm ở bước trước
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.subheader("🎲 Dự báo xác suất (Monte Carlo - 100 kịch bản)")
    sims = MathEngine.monte_carlo_simulation(data)
    fig_mc = go.Figure()
    for i in range(len(sims)):
        fig_mc.add_trace(go.Scatter(y=sims[i], mode='lines', line=dict(width=1), showlegend=False))
    st.plotly_chart(fig_mc, use_container_width=True)
    st.info("Biểu đồ này cho thấy các hướng đi có thể của giá. Nếu các đường tập trung hướng lên, xác suất tăng giá cao.")

with tab3:
    st.subheader("📐 Các mức hỗ trợ Fibonacci")
    fib = MathEngine.calculate_fibonacci_levels(data)
    for level, value in fib.items():
        st.write(f"**{level}:** {value:,.0f}đ")
    st.progress(0.618) # Hiển thị thanh tỷ lệ vàng