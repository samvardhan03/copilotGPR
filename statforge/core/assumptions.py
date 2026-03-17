from scipy import stats
import pandas as pd
import hashlib
from statforge.core.cache import cache

@cache.cache
def run_assumption_check(data_hash: str, check_type: str, data: pd.Series, **kwargs):
    """
    Cached assumption checks to avoid recomputing on large datasets.
    """
    if check_type == 'shapiro':
        stat, p = stats.shapiro(data.dropna())
        return {'stat': stat, 'p_value': p, 'borderline': 0.04 < p < 0.06}
    elif check_type == 'levene':
        group_data = kwargs.get('group_data', [])
        stat, p = stats.levene(*group_data)
        return {'stat': stat, 'p_value': p, 'borderline': 0.04 < p < 0.06}
    else:
        raise ValueError(f"Unknown check type: {check_type}")

class AssumptionChecker:
    @staticmethod
    def _hash_data(series: pd.Series) -> str:
        # Simple fast hash using pandas built-in hashing and SHA256 sum
        return hashlib.sha256(pd.util.hash_pandas_object(series, index=True).values).hexdigest()
        
    def check_normality(self, data: pd.Series) -> dict:
        h = self._hash_data(data)
        return run_assumption_check(h, 'shapiro', data)
        
    def check_homoscedasticity(self, groups: list[pd.Series]) -> dict:
        h = hashlib.sha256(b''.join(self._hash_data(g).encode() for g in groups)).hexdigest()
        return run_assumption_check(h, 'levene', pd.Series(dtype=float), group_data=groups)
