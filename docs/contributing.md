# Contributing to StatForge

StatForge actively encourages open-source contributions. 

The pipeline strictly routes all `MethodSelector` outputs directly to the `ModelFitter` plugin registry and routes `ResultFormatter` outputs directly to the Jinja2 `ReportBuilder`. 

You can contribute to this ecosystem in two primary ways:

## 1. Expanding the Model Registry

StatForge utilizes a decentralized decorator pattern to dynamically construct its execution paths. You may build custom frequentist (`scipy`, `statsmodels`) or Bayesian (`PyMC`) architectures.

All models must implement `statforge.models.registry.BaseModel`.

### API Implementation Example:

```python
from statforge.models.registry import BaseModel, register
import pymc as pm

@register('custom_bayesian_model')
class CustomBayesianModel(BaseModel):
    """Docstring describing the specific parameterizations."""
    
    def fit(self, data, config: dict):
        """
        Implementation must accept the `pandas.DataFrame` and `statforge_config.yaml` dict.
        Must execute the sampler and store the trace internally.
        """
        pass
        
    def effect_size(self) -> dict:
        """
        Calculates and returns the specific effect size.
        Must return a structured dict containing at minimum the `label` key 
        (e.g., small, medium, strong, inconclusive).
        """
        return {"bayesian_effect": 1.2, "label": "strong"}
```

Once defined, drop this `.py` file into `~/.statforge/plugins/`, and the cli runner will automatically identify 'custom_bayesian_model' as an available analytical component.

## 2. Adding Journal Templates

To contribute specific journal publication layouts (e.g., Nature, PLOS ONE, APA7), construct a new Jinja2 template mapping to the `ResultFormatter` extraction schema.

Templates live conceptually in `statforge/report/templates/`.

### Expected Injections

The `ReportBuilder` injects a consolidated data dictionary `results` into the Jinja context. Ensure your `template_name.html.j2` or `template_name.tex.j2` accesses the following schema:

*   `results.methods_text`: A plain-text synthesis from `MethodsBuilder` outlining the decision log and prior rationales.
*   `results.table_rows`: The iterable sequence of analysis results, already formatted appropriately. 

```html
<!-- Example: custom_journal.html.j2 -->
<div class="methodology-section">
    <h2>Methods</h2>
    <!-- The MethodsBuilder constructs the full analytical rationale here -->
    <p>{{ results.get('methods_text', '') }}</p>
</div>

<div class="results-table">
    <table>
      {% for row in results.table_rows %}
        <tr>
            <td>{{ row[0] }}</td>
            <td>{{ row[1] }}</td>
        </tr>
      {% endfor %}
    </table>
</div>
```

Ensure unit tests correctly traverse your new `.j2` structure utilizing mock formatted results prior to opening a Pull Request.
