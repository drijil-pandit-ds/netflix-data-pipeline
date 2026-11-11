import pandas as pd
import numpy as np
from supabase import create_client
import sys

# Hardcode your credentials here ONLY for your local data migration setup.
# Do NOT upload your real keys to GitHub! Use environment variables or placeholders if public.
SUPABASE_URL = "YOUR_SUPABASE_PROJECT_URL" 
SUPABASE_KEY = "YOUR_SUPABASE_ANON_KEY"

def clean_and_upload(input_path):
    print("🚀 Starting Backend Data ETL Pipeline...")
    
    # Extract
    df = pd.read_csv(input_path)
    
    # Transform
    df['director'] = df['director'].fillna('Unknown')
    df['cast'] = df['cast'].fillna('Unknown Cast')
    df['country'] = df['country'].fillna('Unknown Country')
    df.dropna(subset=['date_added', 'duration', 'rating'], inplace=True)
    
    df['date_added'] = df['date_added'].str.strip()
    df['date_added'] = pd.to_datetime(df['date_added'], format='%B %d, %Y', errors='coerce')
    df.dropna(subset=['date_added'], inplace=True)
    
    df['year_added'] = df['date_added'].dt.year.astype(int)
    df['month_added'] = df['date_added'].dt.strftime('%B')
    df['title'] = df['title'].str.strip()
    
    # Convert dates to string format for pure JSON database transfer
    df['date_added'] = df['date_added'].astype(str)
    
    # Load into Supabase
    print("⚡ Connecting to Supabase Cloud database...")
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    
    records = df.to_dict(orient='records')
    print(f"📦 Uploading {len(records)} handled rows to 'netflix_titles' table...")
    
    # Upload in chunks of 200 to prevent cloud payload errors
    chunk_size = 200
    for i in range(0, len(records), chunk_size):
        chunk = records[i:i + chunk_size]
        try:
            supabase.table("netflix_titles").insert(chunk).execute()
        except Exception as e:
            print(f"⚠️ Chunk failure at index {i}: {e}")
            sys.exit(1)
            
    print("✅ Successfully cleaned, structured, and synced data to Supabase Database!")

if __name__ == "__main__":
    clean_and_upload('data/raw_netflix_titles.csv')
              
