import pandas as pd

class PriorAdvisor:
    """Auto-suggests data-driven weakly informative priors and runs prior sensitivity analyses."""
    
    def suggest(self, variable: str, data: pd.Series) -> dict:
        sd = data.std()
        mu = data.mean()
        n = len(data)
        
        return {
            'distribution': 'Normal',
            'mu': round(float(mu), 3),
            'sigma': round(float(sd * 2), 3),
            'rationale': (f"Weakly informative: mu=observed mean, "
                          f"sigma=2x observed SD. Covers plausible range "
                          f"without strong constraint (n={n}).")
        }

SENSITIVITY_VARIANTS = {
    'uninformative': lambda sd: sd * 10,
    'weakly_informative': lambda sd: sd * 2,  # default
    'informative': lambda sd: sd * 0.5
}
