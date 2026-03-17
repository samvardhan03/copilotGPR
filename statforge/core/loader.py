import pandas as pd
import pyreadstat
from pathlib import Path
from typing import Union

class DataLoader:
    """Handles dynamic loading of tabular data formats (CSV, Excel, SPSS, Parquet)."""
    
    @staticmethod
    def load(file_path: Union[str, Path]) -> pd.DataFrame:
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")
            
        ext = path.suffix.lower()
        if ext == '.csv':
            return pd.read_csv(path)
        elif ext in ['.xls', '.xlsx']:
            return pd.read_excel(path)
        elif ext == '.sav':
            df, _ = pyreadstat.read_sav(path)
            return df
        elif ext == '.parquet':
            return pd.read_parquet(path)
        else:
            raise ValueError(f"Unsupported file format: {ext}")
