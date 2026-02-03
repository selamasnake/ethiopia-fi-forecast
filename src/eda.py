import pandas as pd
from typing import List, Optional

class EDA:
    """
    Class to manage Financial Inclusion datasets for exploratory data analysis.
    """

    def __init__(self):
        self.main = pd.DataFrame()
        self.impacts = pd.DataFrame()
    
    def load_data(self, main_path: str, impacts_path: str):
        """Load main and impact datasets from CSV files."""
        self.main = pd.read_csv(main_path)
        self.impacts = pd.read_csv(impacts_path)
        print(f"Loaded main dataset with shape {self.main.shape}")
        print(f"Loaded impacts dataset with shape {self.impacts.shape}")
    
    def preprocess_data(self):
        """Preprocess datasets: convert dates and numeric fields."""
        if 'observation_date' in self.main.columns:
            self.main['observation_date'] = pd.to_datetime(self.main['observation_date'], errors='coerce')
        numeric_cols = ['value_numeric']
        for col in numeric_cols:
            if col in self.main.columns:
                self.main[col] = pd.to_numeric(self.main[col], errors='coerce')
        print("Preprocessing complete: dates and numeric fields converted.")

    def filter_records(self, record_type: Optional[str] = None, pillar: Optional[str] = None):
        """Filter main dataset by record_type and/or pillar."""
        df = self.main
        if record_type:
            df = df[df['record_type'] == record_type]
        if pillar:
            df = df[df['pillar'] == pillar]
        return df

    def summarize_by(self, column: str):
        """Return value counts for a specified column in the main dataset."""
        if column in self.main.columns:
            return self.main[column].value_counts(dropna=False)
        else:
            raise ValueError(f"{column} not found in main dataset.")
    
    def temporal_coverage(self, indicators: Optional[List[str]] = None):
        """
        Summarize which years have data for which indicators.
        """
        obs = self.main[self.main['record_type'] == 'observation'].copy()
        obs['year'] = obs['observation_date'].dt.year
        if indicators:
            obs = obs[obs['indicator_code'].isin(indicators)]
        coverage = obs.groupby(['indicator_code', 'year']).size().unstack(fill_value=0)
        return coverage
    
    def confidence_distribution(self):
        """Return counts of confidence levels."""
        return self.summarize_by('confidence')
    
    def identify_sparse_indicators(self, min_count: int = 2):
        """Return indicators with fewer than `min_count` observations."""
        counts = self.main[self.main['record_type'] == 'observation']['indicator_code'].value_counts()
        sparse = counts[counts < min_count]
        return sparse

    def merge_impacts(self):
        """
        Merge impact_links with their parent events to see the full relationships.
        Returns merged DataFrame.
        """
        events = self.main[self.main['record_type'] == 'event'][['record_id','indicator','category','observation_date']]
        merged = self.impacts.merge(events, left_on='parent_id', right_on='record_id', how='left', suffixes=('_impact','_event'))
        return merged
