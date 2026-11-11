# 🎬 Netflix End-To-End cloud Data Analytics Pipeline

A production-grade **IT Final Year Project** built around a full-stack data pipeline. This setup ingests raw metadata, cleans parameters via an automated Python script, migrates dataset matrices to a live **Supabase Cloud Database (PostgreSQL)**, and outputs an executive visual analytics platform via **Streamlit Cloud**.

## 📐 Enterprise Architecture Map
`[ Kaggle Data Source ]` ➡️ `[ Python ETL Script ]` ➡️ `[ Supabase Cloud Postgres ]` ➡️ `[ Live Streamlit Dashboard ]`

## 🚀 Live Hosted Application System
🔗 **[INSERT YOUR LIVE STREAMLIT LINK HERE]**

## 🔧 Installation & Manual System Initiation
1. Clone Project locally:
   ```bash
   git clone https://github.com
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run backend data pipeline migration to Cloud Database:
   ```bash
   python src/data_cleaning.py
   ```
4. Boot up local platform view:
   ```bash
   streamlit run app.py
   ```
