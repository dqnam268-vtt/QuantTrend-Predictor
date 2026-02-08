import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from src.data_engine import DataEngine
from src.math_engine import MathEngine
from src.ml_engine import MLEngine

# Khởi tạo
data_eng = DataEngine()
math_eng = MathEngine()
ml_eng = MLEngine(sequence_length=60)

st.set_page_config(page_title="QuantTrend Pro", layout="wide")
st.title("📈 QuantTrend Pro: Backtesting & Real-time Prediction")

# Sidebar
selected_stock = st.sidebar.selectbox("Mã chứng khoán", ['FPT', 'HT1', 'HPG', 'VIC'])
test_size = st.sidebar.slider("Dữ liệu Backtest (số phiên)", 20, 100, 60)
run_bt = st.sidebar.button("Chạy Backtesting & Dự báo")

# Load & Prepare Data
df_raw = data_eng.fetch_historical_data(selected_stock)

if df_raw is not None:
    # Feature Engineering từ ml_engine
    df = ml_eng.add_indicators(df_raw.copy())
    
    # --- UI: Biểu đồ chính ---
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['time'], y=df['close'], name="Giá thực tế", line=dict(color='rgba(0,0,255,0.5)')))

    if run_bt:
        with st.spinner('Đang chạy mô hình học máy đa biến...'):
            # 1. Huấn luyện mô hình
            x_train, y_train = ml_eng.prepare_multivariate_data(df)
            ml_eng.build_advanced_model(input_shape=(x_train.shape[1], x_train.shape[2]))
            ml_eng.model.fit(x_train, y_train, epochs=15, batch_size=32, verbose=0)
            
            # 2. Backtesting: Dự báo lại các phiên gần đây
            backtest_preds = []
            actual_values = df['close'].tail(test_size).values
            
            # Dự báo trượt cho n phiên cuối
            for i in range(test_size, 0, -1):
                temp_df = df.iloc[:len(df)-i]
                p = ml_eng.predict_future(temp_df)
                backtest_preds.append(p)
            
            # 3. Dự báo tương lai (phiên tiếp theo)
            future_pred = ml_eng.predict_future(df)
            
            # 4. Vẽ đường Backtest
            bt_time = df['time'].tail(test_size)
            fig.add_trace(go.Scatter(x=bt_time, y=backtest_preds, 
                                     name="Dự báo Backtest", 
                                     line=dict(color='red', dash='dot')))
            
            # --- Hiển thị kết quả đánh giá ---
            st.subheader("📊 Kết quả kiểm định (Backtesting)")
            
            # Tính sai số MAPE
            mape = np.mean(np.abs((actual_values - backtest_preds) / actual_values)) * 100
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Độ chính xác lịch sử", f"{100 - mape:.2f}%")
            col2.metric("Giá dự báo phiên tới", f"{future_pred:,.0f} VND")
            col3.metric("Trạng thái", "TĂNG" if future_pred > df['close'].iloc[-1] else "GIẢM")

    # Hiển thị biểu đồ
    st.plotly_chart(fig, use_container_width=True)
    
    # Hiển thị bảng dữ liệu toán học
    with st.expander("Xem dữ liệu tính toán chi tiết"):
        st.dataframe(df.tail(10))

else:
    st.error("Không thể tải dữ liệu. Vui lòng kiểm tra kết nối vnstock.")