import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import joblib
import pandas as pd

# 1. Setup User Data
names = ["User 1", "User 2", "User 3", "User 4"]
usernames = ["222689F", "222710N", "222111L", "222333K"]

# For the first run, passwords are the same as usernames
# We 'hash' them so they aren't stored as plain text (Security Best Practice)
hashed_passwords = stauth.Hasher(usernames).generate()

# 2. Create the Credentials Dictionary
credentials = {"usernames": {}}
for name, username, password in zip(names, usernames, hashed_passwords):
    credentials["usernames"][username] = {
        "name": name,
        "password": password
    }

# 3. Initialize Authenticator
authenticator = stauth.Authenticate(
    credentials,
    "construction_delay_cookie", # Cookie name to keep user logged in
    "signature_key",             # Key for the cookie
    cookie_expiry_days=30
)

# 4. Render the Login Widget
name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status == False:
    st.error("Username/password is incorrect")
elif authentication_status == None:
    st.warning("Please enter your username and password")
elif authentication_status:
    # --- LOGGED IN AREA ---
    
    # Sidebar features
    authenticator.logout("Logout", "sidebar")
    st.sidebar.title(f"Welcome {name}")
    
    # ALLOW PASSWORD CHANGE
    if st.sidebar.checkbox("Change Password"):
        try:
            if authenticator.reset_password(username, 'Change Password'):
                st.sidebar.success('Password modified successfully')
        except Exception as e:
            st.sidebar.error(e)

    # --- YOUR ANN MODEL CODE STARTS HERE ---
    st.title("🏗️ High-Rise Delay Prediction (ANN)")
    
    # Load your models
    model = joblib.load('ann_model.pkl')
    scaler = joblib.load('scaler.pkl')
    model_columns = joblib.load('model_columns_svm.pkl')

    # (Add your sliders and prediction logic here exactly as before...)
