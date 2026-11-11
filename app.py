import streamlit as st
import pandas as pd
from supabase import create_client

SUPABASE_URL = "YOUR_SUPABASE_PROJECT_URL"
SUPABASE_KEY = "YOUR_SUPABASE_ANON_KEY"

@st.cache_data # Caches data so your website loads instantly
def load_live_supabase_data():
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    # Query all rows from the cloud table
    response = supabase.table("netflix_titles").select("*").execute()
    return pd.DataFrame(response.data)

st.title("🎬 Live Supabase Cloud-Linked Netflix Dashboard")

try:
    df = load_live_supabase_data()
    st.success(f"⚡ Connected Live! Successfully retrieved {len(df)} rows from Supabase Database.")
    
    # Display the backend database to your professor live
    st.subheader("🔍 Real-time Database Inspect Engine")
    st.dataframe(df.head(10))
    
    # Insert your visualization plots here using 'df' variable...
    
except Exception as e:
    st.error(f"Failed to connect to Supabase: {e}")
  
