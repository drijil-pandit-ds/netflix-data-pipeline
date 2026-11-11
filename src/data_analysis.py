import pandas as pd
from supabase import create_client

class CloudNetflixAnalyzer:
    """
    Analytical engine handling relational database queries and data structures 
    for the Cloud Netflix Data Pipeline Dashboard.
    """
    def __init__(self, supabase_url: str, supabase_key: str):
        """Initializes secure connection to the Supabase Client Engine."""
        self.supabase = create_client(supabase_url, supabase_key)

    def fetch_summary_metrics(self) -> dict:
        """
        Queries cloud tables to extract top-level Key Performance Indicators (KPIs).
        Optimizes network payloads by returning analytical aggregates.
        """
        # Retrieve all records from cloud instance
        response = self.supabase.table("netflix_titles").select("show_id, type").execute()
        df = pd.DataFrame(response.data)
        
        if df.empty:
            return {"total": 0, "movies": 0, "shows": 0}
            
        metrics = {
            "total": len(df),
            "movies": len(df[df['type'] == 'Movie']),
            "shows": len(df[df['type'] == 'TV Show'])
        }
        return metrics

    def get_content_distribution(self) -> pd.Series:
        """Returns the distribution ratio between Movies and TV Shows."""
        response = self.supabase.table("netflix_titles").select("type").execute()
        df = pd.DataFrame(response.data)
        return df['type'].value_counts() if not df.empty else pd.Series(dtype=int)

    def get_top_ratings(self, limit: int = 8) -> pd.Series:
        """Extracts and sorts the highest density content audience ratings (e.g., TV-MA, PG-13)."""
        response = self.supabase.table("netflix_titles").select("rating").execute()
        df = pd.DataFrame(response.data)
        return df['rating'].value_counts().head(limit) if not df.empty else pd.Series(dtype=int)

    def get_top_genres(self, limit: int = 10) -> pd.Series:
        """
        Performs an array flattening (explode) operation on mixed string categories
        to accurately count individual genre distribution across the entire matrix.
        """
        response = self.supabase.table("netflix_titles").select("listed_in").execute()
        df = pd.DataFrame(response.data)
        
        if df.empty or 'listed_in' not in df.columns:
            return pd.Series(dtype=int)
            
        # Explode logic: splits "Sci-Fi, Dramas" into separate instances for precise aggregation
        genres = df['listed_in'].str.split(', ').explode()
        return genres.value_counts().head(limit)

    def get_raw_sample(self, rows: int = 15) -> pd.DataFrame:
        """Queries a slice of the structural dataset schema for visual validation panels."""
        response = self.supabase.table("netflix_titles").select("show_id, type, title, country, date_added, year_added").limit(rows).execute()
        return pd.DataFrame(response.data)
  
