import streamlit as st
import streamlit_authenticator as stauth
import pandas as pd
import joblib

# --- 1. USER AUTHENTICATION SETUP ---
# Pre-defining the credentials with the usernames you provided
credentials = {
    "usernames": {
        "222689F": {"name": "Nirmal", "password": "222689F"},
        "222710N": {"name": "Lakshan", "password": "222710N"},
        "222111L": {"name": "Wenura", "password": "222111L"},
        "222333K": {"name": "UoM User", "password": "222333K"}
    }
}

# The latest version of the library hashes the passwords in the dict directly
stauth.Hasher.hash_passwords(credentials)

# Initialize the Authenticator
authenticator = stauth.Authenticate(
    credentials,
    "construction_delay_cookie",
    "signature_key_123",
    cookie_expiry_days=30
)

# --- 2. RENDER LOGIN SCREEN ---
authenticator.login()

if st.session_state["authentication_status"] is False:
    st.error("Username/password is incorrect")
elif st.session_state["authentication_status"] is None:
    st.warning("Please enter your username and password")
elif st.session_state["authentication_status"]:
    
    # --- 3. LOGGED IN AREA (Everything below happens after login) ---
    
    # Sidebar Navigation & Logout
    st.sidebar.title(f"Welcome, {st.session_state['name']}")
    authenticator.logout("Logout", "sidebar")
    
    # Password Reset Feature in Sidebar
    if st.sidebar.checkbox("Reset Password"):
        try:
            if authenticator.reset_password(st.session_state["username"], 'Reset Password'):
                st.sidebar.success('Password modified successfully')
        except Exception as e:
            st.sidebar.error(e)

    # --- 4. THE ANN MODEL INTERFACE ---
    st.title("🏗️ High-Rise Delay Prediction Model (ANN)")
    st.markdown("""
    This model uses an **Artificial Neural Network** to predict construction delays 
    based on historical high-rise project data in Sri Lanka.
    """)

    # Load the Model, Scaler, and Columns
    try:
        model = joblib.load('ann_model.pkl')
        scaler = joblib.load('scaler.pkl')
        model_columns = joblib.load('model_columns_svm.pkl')
        
        # --- 5. USER INPUTS ---
        col1, col2 = st.columns(2)
        
        with col1:
            p_type = st.selectbox("Project Type", ['Residential', 'Commercial', 'Mixed Development', 'Hotel'])
            area = st.number_input("Total Floor Area (m²)", min_value=100.0, value=2500.0)
        
        with col2:
            floors = st.number_input("Number of Floors", min_value=1, value=15)
            basements = st.number_input("Number of Basement Levels", min_value=0, value=2)

        # --- 6. PREDICTION LOGIC ---
        if st.button("Predict Construction Delay"):
            # Prepare the input row
            input_df = pd.DataFrame(0, index=[0], columns=model_columns)
            
            # Fill numerical values
            input_df['Floor Area (m²)'] = area
            input_df['No. of Floors'] = floors
            # If your model used 'Basements', add it here:
            if 'Basements' in input_df.columns:
                input_df['Basements'] = basements
            
            # Fill One-Hot Encoded Project Type
            target_col = f"Project Type_{p_type}"
            if target_col in input_df.columns:
                input_df[target_col] = 1
            
            # SCALE the input (Crucial for ANN)
            input_scaled = scaler.transform(input_df)
            
            # Predict
            prediction = model.predict(input_scaled)[0]
            
            # Display Results
            st.markdown("---")
            if prediction > 0:
                st.error(f"### Predicted Delay: {prediction:.1f} Days")
                st.write("Consider increasing your contingency buffer for this project.")
            else:
                st.success(f"### Predicted Delay: 0 Days (On Schedule)")
                st.write("The model suggests this project configuration is low-risk for delays.")

    except FileNotFoundError:
        st.error("Model files not found. Please ensure 'ann_model.pkl', 'scaler.pkl', and 'model_columns_svm.pkl' are in your GitHub repository.")
