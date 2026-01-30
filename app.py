import streamlit as st
import pandas as pd
import logic

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="De-eagle Global Intel", layout="wide", page_icon="🦅")

# --- 2. THE TECH UI & BACKGROUND (CSS) ---
st.markdown("""
    <style>
    /* 1. BACKGROUND IMAGE */
    .stApp {
        background-image: linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.9)), 
                          url("https://images.unsplash.com/photo-1579304724896-80415d658525?q=80&w=2546&auto=format&fit=crop");
        background-attachment: fixed;
        background-size: cover;
    }

    /* 2. TECH FONTS */
    h1, h2, h3, h4, .stMetricLabel { 
        color: #FFD700 !important; 
        font-family: 'Courier New', Courier, monospace; 
        text-shadow: 0px 0px 10px rgba(255, 215, 0, 0.5);
    }
    
    /* 3. GLASS SIDEBAR */
    [data-testid="stSidebar"] {
        background-color: rgba(0, 0, 0, 0.6) !important;
        border-right: 1px solid #FFD700;
        backdrop-filter: blur(10px);
    }
    
    /* 4. TABLES & INPUTS */
    .stDataFrame { border: 1px solid #FFD700; background-color: rgba(0, 0, 0, 0.5); }
    .stTextInput > div > div > input { color: #FFD700; background-color: rgba(0,0,0,0.8); }
    div[data-testid="stMetricValue"] { color: #FFD700 !important; text-shadow: 0px 0px 10px #FFD700; font-family: 'Courier New'; }
    </style>
""", unsafe_allow_html=True)

# --- 3. SIDEBAR CONTROLS ---
with st.sidebar:
    st.image("https://em-content.zobj.net/source/microsoft-teams/337/shield_1f6e1.png", width=60)
    st.title("COMMAND CENTER")
    st.markdown("---")
    
    # A. NETWORK SELECTOR
    selected_chain = st.selectbox(
        "1. SELECT NETWORK:",
        ["Ethereum", "Monad", "Sei", "Base", "Arbitrum", "Optimism", "Linea"]
    )
    
    st.markdown("---")
    
    # B. MODE SELECTOR (Global vs Target)
    scan_mode = st.radio("2. SCAN MODE:", ["GLOBAL MONITOR", "TARGET PROJECT"])
    
    target_contract = ""
    if scan_mode == "TARGET PROJECT":
        st.warning("⚠️ ENTER CONTRACT ADDRESS BELOW:")
        target_contract = st.text_input("CONTRACT ADDR:", placeholder="0x...")
    
    st.markdown("---")
    if st.button("⚡ REFRESH INTEL"):
        st.cache_data.clear()

# --- 4. MAIN DASHBOARD ---
st.markdown(f"# 🦅 DE-EAGLE // {selected_chain.upper()}")

# LOAD DATA
with st.spinner(f"ESTABLISHING UPLINK TO {selected_chain.upper()} NODE..."):
    df = logic.fetch_chain_data(selected_chain)
    
    # Prepare Data Containers
    display_df = pd.DataFrame()
    bad_guys = []
    
    if not df.empty:
        df.columns = [c.lower() for c in df.columns]

        # LOGIC: FILTERING
        if scan_mode == "GLOBAL MONITOR":
            st.markdown(f"### 📡 GLOBAL NETWORK SURVEILLANCE ({selected_chain})")
            for col in ['sender', 'wallet_address', 'from', 'address']:
                if col in df.columns:
                    display_df = df.copy()
                    bad_guys = df[col].unique().tolist()
                    break
                    
        elif scan_mode == "TARGET PROJECT":
            st.markdown(f"### 🎯 TARGET LOCK: {target_contract if target_contract else 'WAITING...'}")
            
            if target_contract:
                # Filter for interactions with the target contract
                # We check 'to', 'receiver', or 'contract_address'
                to_col = next((c for c in ['to', 'receiver', 'contract_address'] if c in df.columns), None)
                from_col = next((c for c in ['from', 'sender', 'wallet_address'] if c in df.columns), None)
                
                if to_col and from_col:
                    project_df = df[df[to_col].str.lower() == target_contract.lower()]
                    
                    if not project_df.empty:
                        display_df = project_df
                        bad_guys = project_df[from_col].unique().tolist()
                    else:
                        st.info(f"0 THREATS DETECTED TARGETING {target_contract} IN CURRENT DATA STREAM.")
                else:
                    st.error("DATA STREAM ERROR: MISSING 'RECEIVER' COLUMN.")
            else:
                st.info("👈 AWAITING TARGET COORDINATES IN SIDEBAR...")

# --- 5. DISPLAY METRICS & GRID ---
if bad_guys:
    # Metrics Bar
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("HOSTILES DETECTED", len(bad_guys))
    col2.metric("SCAN MODE", scan_mode)
    col3.metric("THREAT LEVEL", "CRITICAL")
    col4.metric("SYSTEM STATUS", "ONLINE")
    
    st.divider()
    
    # Data Table
    st.markdown("### 🧬 FORENSIC EVIDENCE")
    st.dataframe(display_df, use_container_width=True, height=500)

elif scan_mode == "GLOBAL MONITOR" and df.empty:
    st.warning("NO DATA STREAM. CHECK LOGIC.PY CONFIGURATION.")