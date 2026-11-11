import pandas as pd
from supabase import create_client

class CloudNetflixAnalyzer:
    """
    Decoupled Object-Oriented Analytical Query Optimization Engine.
    Executes calculations directly against cloud table targets.
    """
    def __init__(self, target_url: str, security_key: str):
        """Builds state-managed integration client."""
        self.supabase = create_client(target_url, security_key)

    def fetch_dashboard_kpis(self) -> dict:
        """Computes summary scorecard metrics across data types."""
        query_response = self.supabase.table("netflix_titles").select("show_id, type").execute()
        dataframe_matrix = pd.DataFrame(query_response.data)
        
        if dataframe_matrix.empty:
            return {"total": 0, "movies": 0, "shows": 0}
            
        return {
            "total": len(dataframe_matrix),
            "movies": len(dataframe_matrix[dataframe_matrix['type'] == 'Movie']),
            "shows": len(dataframe_matrix[dataframe_matrix['type'] == 'TV Show'])
        }

    def compute_production_ratio(self) -> pd.Series:
        """Extracts production density volume allocation."""
        query_response = self.supabase.table("netflix_titles").select("type").execute()
        dataframe_matrix = pd.DataFrame(query_response.data)
        return dataframe_matrix['type'].value_counts() if not dataframe_matrix.empty else pd.Series(dtype=int)

    def extract_top_genres(self, rank_limit: int = 10) -> pd.Series:
        """Performs column explosion transformations over nested genre string arrays."""
        query_response = self.supabase.table("netflix_titles").select("listed_in").execute()
        dataframe_matrix = pd.DataFrame(query_response.data)
        
        if dataframe_matrix.empty or 'listed_in' not in dataframe_matrix.columns:
            return pd.Series(dtype=int)
            
        flattened_genres = dataframe_matrix['listed_in'].str.split(', ').explode()
        return flattened_genres.value_counts().head(rank_limit)

    def get_database_preview(self, query_limit: int = 15) -> pd.DataFrame:
        """Acquires subset slice of structural relational grid for auditing validation panels."""
        query_response = self.supabase.table("netflix_titles").select(
            "show_id, type, title, country, date_added, year_added"
        ).limit(query_limit).execute()
        return pd.DataFrame(query_response.data)
