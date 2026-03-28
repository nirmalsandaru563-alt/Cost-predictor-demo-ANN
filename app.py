import streamlit as st
import streamlit_authenticator as stauth
import joblib
import pandas as pd

# 1. Setup User Data
names = ["User 1", "User 2", "User 3", "User 4"]
usernames = ["222689F", "222710N", "222111L", "222333K"]

# NEW METHOD: We hash the passwords individually
# Note: In the new version, Hasher expects a list and returns a list
hashed_passwords = stauth.Hasher(usernames).generate() 

# 2. Create the Credentials Dictionary
# The library now requires 'emails' to be present (even if empty)
credentials = {"usernames": {}}
for name, username, password in zip(names, usernames, hashed_passwords):
    credentials["usernames"][username] = {
        "name": name,
        "password": password,
        "email": f"{username}@uom.lk" # Added a placeholder email
    }

# 3. Initialize Authenticator
# The new version uses 'cookie_name' and 'key' as keyword arguments
authenticator = stauth.Authenticate(
    credentials,
    "construction_delay_cookie", 
    "signature_key",             
    cookie_expiry_days=30
)

# 4. Render the Login Widget
# In the new version, it returns a dict of info
try:
    authenticator.login()
except Exception as e:
    st.error(e)

if st.session_state["authentication_status"] == False:
    st.error("Username/password is incorrect")
elif st.session_state["authentication_status"] == None:
    st.warning("Please enter your username and password")
elif st.session_state["authentication_status"]:
    # --- LOGGED IN AREA ---
    authenticator.logout("Logout", "sidebar")
    st.sidebar.title(f"Welcome {st.session_state['name']}")
    
    # Rest of your prediction code goes here...
    
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
