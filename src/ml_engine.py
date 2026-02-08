import numpy as np
import pandas as pd
from sklearn.preprocessing import RobustScaler
import tensorflow as tf
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.layers import LSTM, Dense, Dropout, Input, Attention, Concatenate, GlobalAveragePooling1D

class MLEngine:
    def __init__(self, sequence_length=60):
        self.sequence_length = sequence_length
        # RobustScaler giúp xử lý outliers tốt hơn MinMaxScaler cho dữ liệu tài chính
        self.scaler = RobustScaler()
        self.model = None

    def add_indicators(self, df):
        """Feature Engineering: Thêm các biến số toán học vào đầu vào"""
        # 1. RSI (Relative Strength Index)
        delta = df['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df['RSI'] = 100 - (100 / (1 + rs))
        
        # 2. Volatility (Độ biến động)
        df['volatility'] = df['close'].rolling(window=20).std()
        
        # 3. Log Return (Tỷ suất sinh lời log - giúp dữ liệu dừng hơn)
        df['log_return'] = np.log(df['close'] / df['close'].shift(1))
        
        return df.fillna(0)

    def prepare_multivariate_data(self, df):
        """Chuẩn bị dữ liệu đa biến [Close, Volume, RSI, Volatility]"""
        features = ['close', 'volume', 'RSI', 'volatility']
        scaled_data = self.scaler.fit_transform(df[features])
        
        x_train, y_train = [], []
        for i in range(self.sequence_length, len(scaled_data)):
            x_train.append(scaled_data[i-self.sequence_length:i])
            y_train.append(scaled_data[i, 0]) # Dự báo giá Close (cột 0)
            
        return np.array(x_train), np.array(y_train)

    def build_advanced_model(self, input_shape):
        """Thiết kế mạng LSTM với cơ chế Attention đơn giản"""
        inputs = Input(shape=input_shape)
        
        # Lớp LSTM 1
        lstm_out = LSTM(100, return_sequences=True)(inputs)
        lstm_out = Dropout(0.2)(lstm_out)
        
        # Lớp LSTM 2
        lstm_out2 = LSTM(100, return_sequences=True)(lstm_out)
        
        # Cơ chế Self-Attention: Tập trung vào các thời điểm quan trọng trong quá khứ
        query = Dense(100)(lstm_out2)
        value = Dense(100)(lstm_out2)
        attention_out = Attention()([query, value])
        
        # Kết hợp và Pooling
        avg_pool = GlobalAveragePooling1D()(attention_out)
        
        # Output layers
        dense1 = Dense(50, activation='relu')(avg_pool)
        outputs = Dense(1)(dense1)
        
        model = Model(inputs=inputs, outputs=outputs)
        
        # Sử dụng Huber Loss để tối ưu hóa độ chính xác toán học
        model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.001), 
                      loss=tf.keras.losses.Huber())
        self.model = model
        return model

    def predict_future(self, df):
        """Dự báo giá cho phiên tiếp theo dựa trên đa biến"""
        features = ['close', 'volume', 'RSI', 'volatility']
        last_window = df[features].tail(self.sequence_length).values
        last_window_scaled = self.scaler.transform(last_window)
        
        X_test = np.array([last_window_scaled])
        pred_scaled = self.model.predict(X_test)
        
        # Nghịch đảo chuẩn hóa (chỉ cho cột giá Close)
        # Tạo một dummy array để inverse transform chính xác
        dummy = np.zeros((1, len(features)))
        dummy[0, 0] = pred_scaled[0, 0]
        pred_final = self.scaler.inverse_transform(dummy)[0, 0]
        
        return pred_final