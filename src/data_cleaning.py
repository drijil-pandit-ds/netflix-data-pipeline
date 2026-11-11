import pandas as pd
import numpy as np
from supabase import create_client
import sys

# Replace these with your actual credentials from your Supabase Dashboard -> Project Settings -> API
SUPABASE_URL = "YOUR_SUPABASE_PROJECT_URL" 
SUPABASE_KEY = "YOUR_SUPABASE_ANON_KEY"

def clean_and_upload_pipeline(input_csv_path):
    print("🚀 Initiating Backend Data ETL & Cloud Sync Engine...")
    
    # --- PHASE 1: EXTRACT ---
    try:
        df = pd.read_csv(input_csv_path)
    except FileNotFoundError:
        print(f"❌ Critical Error: Base dataset missing at '{input_csv_path}'. Upload your Kaggle CSV.")
        sys.exit(1)
        
    # --- PHASE 2: TRANSFORM (DATA CLEANING) ---
    # Impute missing textual strings
    df['director'] = df['director'].fillna('Unknown')
    df['cast'] = df['cast'].fillna('Unknown Cast')
    df['country'] = df['country'].fillna('Unknown Country')
    
    # Drop records containing critical structural gaps
    df.dropna(subset=['date_added', 'duration', 'rating'], inplace=True)
    
    # Standardize textual timestamps to standard Datetime format matrices
    df['date_added'] = df['date_added'].str.strip()
    df['date_added'] = pd.to_datetime(df['date_added'], format='%B %d, %Y', errors='coerce')
    df.dropna(subset=['date_added'], inplace=True)
    
    # Feature Engineering: Extract time buckets
    df['year_added'] = df['date_added'].dt.year.astype(int)
    df['month_added'] = df['date_added'].dt.strftime('%B')
    
    # Standardize string formatting
    df['title'] = df['title'].str.strip()
    
    # Cast timestamp variables to strings to fulfill standard JSON database transfer payloads
    df['date_added'] = df['date_added'].astype(str)
    
    # --- PHASE 3: LOAD (SUPABASE SYNCHRONIZATION) ---
    print("⚡ Connecting securely to Cloud PostgreSQL instance via Supabase client...")
    supabase_client = create_client(SUPABASE_URL, SUPABASE_KEY)
    
    # Translate memory Dataframe into record arrays
    records = df.to_dict(orient='records')
    print(f"📦 Transferring {len(records)} handled data matrices to cloud 'netflix_titles' table...")
    
    # Partition records into 200-row chunks to protect maximum server network packet thresholds
    network_chunk_limit = 200
    for block_index in range(0, len(records), network_chunk_limit):
        data_block = records[block_index:block_index + network_chunk_limit]
        try:
            supabase_client.table("netflix_titles").insert(data_block).execute()
        except Exception as database_error:
            print(f"❌ Pipeline Interrupted at index chunk {block_index}: {database_error}")
            sys.exit(1)
            
    print("✅ Complete ETL Pipeline Success! Your backend data is synced live with Supabase.")

if __name__ == "__main__":
    clean_and_upload_pipeline('data/raw_netflix_titles.csv')
