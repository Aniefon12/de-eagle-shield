import pandas as pd
import streamlit as st
from dune_client.client import DuneClient

# SECURITY PROTOCOL:
# The app will look for the key in the "Safe" (Secrets) first.
if "DUNE_API_KEY" in st.secrets:
    DUNE_API_KEY = st.secrets["DUNE_API_KEY"]
else:
    # This prevents the app from crashing if you run it locally without secrets
    DUNE_API_KEY = "TEMP_KEY" 

# ... (Rest of your fetch_chain_data code) ...

# 2. YOUR CHAIN IDs (Zircuit Removed)
CHAIN_IDS = {
    "Ethereum": 6613455,  
    "Monad": 6613487,     
    "Sei": 6613575,
    "Base": 6613427,
    "Arbitrum": 6613610,
    "Optimism": 6613631,
    "Linea": 6614046
}

def fetch_chain_data(chain_name):
    # 1. Get the ID
    query_id = CHAIN_IDS.get(chain_name)
    
    # 2. Safety Check: Did we find an ID?
    if query_id is None:
        st.warning(f"⚠️ Configuration Error: {chain_name} is not set up in logic.py.")
        return pd.DataFrame()

    dune = DuneClient(DUNE_API_KEY)
    
    try:
        # 3. Fetch Data
        results = dune.get_latest_result(query_id)
        df = pd.DataFrame(results.result.rows)
        return df
        
    except Exception as e:
        st.error(f"⚠️ DUNE ERROR ({chain_name}): {e}")
        return pd.DataFrame()