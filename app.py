import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from src.data_analysis import CloudNetflixAnalyzer

# Configure page parameters
st.set_page_config(page_title="Netflix Cloud Data Platform", layout="wide")

st.title("🎬 Full-Stack Netflix Cloud Pipeline Platform")
st.markdown("**IT Final Year Project Presentation Layer** | Architecture: Python ETL ➡️ Supabase Cloud Postgres ➡️ Streamlit")

# --- ENVIRONMENT INTEGRATION SECURE SHIELD ---
try:
    # Safely extracts connection endpoints from hidden cloud production settings
    CLOUD_URL = st.secrets["SUPABASE_URL"]
    CLOUD_KEY = st.secrets["SUPABASE_KEY"]
except Exception:
    st.error("🔒 Security Halt: API Production Connection Secrets are unconfigured within the cloud console.")
    st.info("💡 Deployment Notice: Inject 'SUPABASE_URL' and 'SUPABASE_KEY' inside the Streamlit Advanced Secrets Dashboard Panel.")
    st.stop()

# Initialize decoupled logical calculation module
analytics_engine = CloudNetflixAnalyzer(CLOUD_URL, CLOUD_KEY)

try:
    # Retrieve cloud computing statistics
    kpi_aggregates = analytics_engine.fetch_dashboard_kpis()
    st.success("⚡ Infrastructure Verification: Real-Time Relational Link Synchronized with Supabase Cloud Core!")
    
    # --- UI KPI METRIC GRID GRID ---
    scorecard_col1, scorecard_col2, scorecard_col3 = st.columns(3)
    scorecard_col1.metric("Database Registered Assets", kpi_aggregates["total"])
    scorecard_col2.metric("Total Cinema Movies", kpi_aggregates["movies"])
    scorecard_col3.metric("Total Streaming Shows", kpi_aggregates["shows"])
    
    # --- VISUAL BUSINESS INTELLIGENCE (BI) PORTAL ---
    st.subheader("📊 Relational Database Analytical Distribution Plots")
    visualization_col1, visualization_col2 = st.columns(2)
    
    with visualization_col1:
        st.write("### Platform Inventory Mix")
        production_mix = analytics_engine.compute_production_ratio()
        figure_canvas, axis_object = plt.subplots()
        production_mix.plot(kind='pie', autopct='%1.1f%%', colors=['#E50914', '#221F1F'], ax=axis_object)
        axis_object.set_ylabel('') # Strips ugly margin text tracking
        st.pyplot(figure_canvas)
        
    with visualization_col2:
        st.write("### Leading Volume Program Genres")
        genre_distribution = analytics_engine.extract_top_genres(10)
        figure_canvas, axis_object = plt.subplots()
        sns.barplot(x=genre_distribution.values, y=genre_distribution.index, palette="Reds_r", ax=axis_object)
        st.pyplot(figure_canvas)
        
    # --- UNDER-THE-HOOD SYSTEM INSPECTION FOR EVALUATORS ---
    st.markdown("---")
    st.subheader("🔍 Backend Database Inspection Portal")
    with st.expander("Click to run real-time queries directly against live PostgreSQL Tables"):
        st.write("### Dynamic Schema Output Matrix (Top 15 Rows Sorted via Cloud Primary Key Id)")
        live_table_dataframe = analytics_engine.get_database_preview(15)
        st.dataframe(live_table_dataframe, use_container_width=True)
        
except Exception as connection_error:
    st.error(f"❌ Transmission Fault: Operational data loop could not resolve database streams. Details: {connection_error}")
