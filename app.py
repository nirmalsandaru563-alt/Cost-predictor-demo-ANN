import streamlit as st
import pandas as pd
import joblib

# 1. Load the ANN files
model = joblib.load('ann_model.pkl')
scaler = joblib.load('scaler.pkl')
model_columns = joblib.load('model_columns_svm.pkl')

st.title("🧠 ANN Construction Cost Predictor")

# 2. User Inputs
p_type = st.selectbox("Project Type", ['Residential', 'Commercial', 'Industrial', 'Other'])
area = st.number_input("Floor Area (m²)", value=100.0)
floors = st.number_input("No. of Floors", min_value=1, value=1)

# 3. Create input row and map data
input_df = pd.DataFrame(0, index=[0], columns=model_columns)
input_df['Floor Area (m²)'] = area
input_df['No. of Floors'] = floors
target_col = f"Project Type_{p_type}"
if target_col in input_df.columns:
    input_df[target_col] = 1

# 4. Scale the input (Required for ANN)
input_scaled = scaler.transform(input_df)

# 5. Predict
if st.button("Calculate ANN Estimate"):
    prediction = model.predict(input_scaled)[0]
    st.success(f"### ANN Predicted Cost: {prediction:.2f} LKR Million")
    st.info("ANNs look for deep patterns but need lots of data to be 100% accurate.")
