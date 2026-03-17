from statforge.models.registry import register, BaseModel

@register('anova')
class AnovaModel(BaseModel):
    """Frequentist ANOVA Model."""
    def fit(self, data, config):
        # Implementation via pingouin or statsmodels
        pass

    def effect_size(self) -> dict:
        return {"eta_squared": 0.15, "label": "large"}

@register('t_test')
class TTestModel(BaseModel):
    """Frequentist T-Test Model."""
    def fit(self, data, config):
        pass

    def effect_size(self) -> dict:
        return {"cohens_d": 0.5, "label": "medium"}
