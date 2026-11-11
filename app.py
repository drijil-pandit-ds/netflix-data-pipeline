import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from src.data_analysis import CloudNetflixAnalyzer  # Import your updated engine

st.set_page_config(page_title="Netflix Cloud Pipeline Dashboard", layout="wide")
st.title("🎬 Netflix Full-Stack Data Pipeline Dashboard")

# 1. Establish Secure Credentials Connection
try:
    URL = st.secrets["SUPABASE_URL"]
    KEY = st.secrets["SUPABASE_KEY"]
except Exception:
    st.error("🔒 Streamlit API Database Secrets are missing.")
    st.stop()

# 2. Initialize the Analytical Engine
analyzer = CloudNetflixAnalyzer(URL, KEY)

try:
    # 3. Pull Live KPI Aggregates
    metrics = analyzer.fetch_summary_metrics()
    
    st.success("⚡ Live Connection Established with Supabase Cloud Postgres!")
    
    # Render KPI Cards
    kpi1, kpi2, kpi3 = st.columns(3)
    kpi1.metric("Cloud Registered Titles", metrics["total"])
    kpi2.metric("Total Movies", metrics["movies"])
    kpi3.metric("Total TV Shows", metrics["shows"])
    
    # 4. Render Visual Analytics Layer using Engine functions
    st.subheader("📊 Relational Database Analytics Visuals")
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.write("### Production Strategy Breakdown")
        dist = analyzer.get_content_distribution()
        fig, ax = plt.subplots()
        dist.plot(kind='pie', autopct='%1.1f%%', colors=['#E50914', '#221F1F'], ax=ax)
        st.pyplot(fig)
        
    with col_right:
        st.write("### Top Content Genres")
        genres = analyzer.get_top_genres()
        fig, ax = plt.subplots()
        sns.barplot(x=genres.values, y=genres.index, palette="Reds_r", ax=ax)
        st.pyplot(fig)
        
    # 5. Database Table Preview Module for Professors
    st.markdown("---")
    st.subheader("🔍 Real-time Cloud DB Inspector")
    with st.expander("Click to query live relational tables under-the-hood"):
        sample_df = analyzer.get_raw_sample(15)
        st.dataframe(sample_df)
        
except Exception as err:
    st.error(f"❌ Connection Interrupted: {err}")
