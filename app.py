import streamlit as st
import streamlit_authenticator as stauth
import pandas as pd
import joblib

# --- Credentials Setup ---
credentials = {
    "usernames": {
        "222689F": {"name": "Nirmal", "password": "222689F"},
        "222710N": {"name": "Motta Lamaya", "password": "222710N"},
        "222111L": {"name": "Chandima", "password": "222111L"},
        "222333K": {"name": "UoM User", "password": "222333K"}
    }
}

stauth.Hasher.hash_passwords(credentials)

authenticator = stauth.Authenticate(
    credentials,
    "construction_delay_cookie",
    "signature_key_123",
    cookie_expiry_days=30
)

# --- 1. RENDER LOGIN ---
# This stays at the left margin (Public)
authenticator.login()

# --- 2. AUTHENTICATION LOGIC ---
if st.session_state["authentication_status"] is False:
    st.error("Username/password is incorrect")
elif st.session_state["authentication_status"] is None:
    st.warning("Please enter your username and password")
elif st.session_state["authentication_status"]:
    # --- EVERYTHING FROM HERE DOWN MUST BE INDENTED ---
    
    # 3. Sidebar Setup
    st.sidebar.title(f"Welcome, {st.session_state['name']}")
    authenticator.logout("Logout", "sidebar")

    # 4. Fixed Reset Password (Added 'sidebar' location)
    if st.sidebar.checkbox("Reset Password"):
        try:
            # We must tell the tool to appear in the 'sidebar'
            if authenticator.reset_password(st.session_state["username"], location='sidebar'):
                st.sidebar.success('Password modified successfully')
        except Exception as e:
            st.sidebar.error(f"Error: {e}")

    # 5. Load the ANN files (Now protected inside the login block)
    try:
        model = joblib.load('ann_model.pkl')
        scaler = joblib.load('scaler.pkl')
        model_columns = joblib.load('model_columns_svm.pkl')

        st.title("🧠 ANN Construction Cost Predictor")

        # 6. User Inputs
        p_type = st.selectbox("Project Type", ['Residential', 'Commercial', 'Industrial', 'Other'])
        area = st.number_input("Floor Area (m²)", value=100.0)
        floors = st.number_input("No. of Floors", min_value=1, value=1)

        # 7. Create input row and map data
        input_df = pd.DataFrame(0, index=[0], columns=model_columns)
        input_df['Floor Area (m²)'] = area
        input_df['No. of Floors'] = floors
        
        target_col = f"Project Type_{p_type}"
        if target_col in input_df.columns:
            input_df[target_col] = 1

        # 8. Scale the input
        input_scaled = scaler.transform(input_df)

        # 9. Predict
        if st.button("Calculate ANN Estimate"):
            prediction = model.predict(input_scaled)[0]
            st.success(f"### ANN Predicted Cost: {prediction:.2f} LKR Million")
            st.info("ANNs look for deep patterns but need lots of data to be 100% accurate.")
            
    except Exception as e:
        st.error(f"Could not load model files. Error: {e}")
