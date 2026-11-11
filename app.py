import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from supabase import create_client

st.set_page_config(page_title="Netflix Cloud Pipeline Dashboard", layout="wide")

st.title("🎬 Netflix Full-Stack Data Pipeline Dashboard")
st.markdown("An IT Final Year Project linking a Python ETL architecture to a Supabase Cloud Database.")

# Read production environment keys safely via Streamlit Secrets
try:
    URL = st.secrets["SUPABASE_URL"]
    KEY = st.secrets["SUPABASE_KEY"]
except Exception:
    st.error("🔒 Streamlit API Database Secrets are missing. Please add them to your cloud dashboard settings.")
    st.stop()

@st.cache_data
def get_live_data():
    supabase = create_client(URL, KEY)
    # Pull data using relational cloud queries
    response = supabase.table("netflix_titles").select("*").execute()
    return pd.DataFrame(response.data)

try:
    df = get_live_data()
    st.success(f"⚡ Live Connection Established! Fetched {len(df)} database entries from Supabase Cloud.")
    
    # KPI Grid Matrix
    kpi1, kpi2, kpi3 = st.columns(3)
    kpi1.metric("Cloud Registered Titles", len(df))
    kpi2.metric("Total Movies", len(df[df['type'] == 'Movie']))
    kpi3.metric("Total TV Shows", len(df[df['type'] == 'TV Show']))
    
    # Visual Analytics Layer
    st.subheader("📊 Relational Database Analytics Visuals")
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.write("### Production Strategy Breakdown")
        fig, ax = plt.subplots()
        df['type'].value_counts().plot(kind='pie', autopct='%1.1f%%', colors=['#E50914', '#221F1F'], ax=ax)
        st.pyplot(fig)
        
    with col_right:
        st.write("### Target Audience Rating Distribution")
        fig, ax = plt.subplots()
        sns.countplot(data=df, x='rating', order=df['rating'].value_counts().index[:8], palette="Reds_r", ax=ax)
        plt.xticks(rotation=45)
        st.pyplot(fig)
        
    # Backend verification inspection module for professors
    st.markdown("---")
    st.subheader("🔍 Real-time Cloud DB Inspector")
    with st.expander("Click to query live relational tables under-the-hood"):
        st.dataframe(df[['show_id', 'type', 'title', 'country', 'date_added', 'year_added']].head(15))
        
except Exception as err:
    st.error(f"❌ Connection Interrupted: Failed to parse structural data layers. {err}")
