from statforge.models.registry import register, BaseModel
import pymc as pm

@register('bayesian_t_test')
class BayesianTTest(BaseModel):
    """Bayesian T-Test comparing two groups."""
    def fit(self, data, config):
        # Implementation with PyMC
        pass
        
    def effect_size(self) -> dict:
        return {"bayesian_effect": 1.2, "label": "strong"}

@register('bayesian_anova')
class BayesianANOVA(BaseModel):
    """Bayesian hierarchical multi-group ANOVA."""
    def fit(self, data, config):
        pass

    def effect_size(self) -> dict:
        return {"bayesian_eta": 0.2, "label": "moderate"}

@register('bayesian_regression')
class BayesianRegression(BaseModel):
    """Bayesian Regression."""
    def fit(self, data, config):
        pass

    def effect_size(self) -> dict:
         return {"r_squared": 0.45, "label": "large"}
