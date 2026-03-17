def build_methods_text(pipeline_log: dict) -> str:
    """Synthesizes a plain-text methodology section from the pipeline's decision log."""
    template = (
        "Data were analysed using {test_full_name} "
        "(StatForge v{version}; {citation}). "
        "{assumption_rationale} "
        "The significance threshold was set at α = {alpha}. "
        "Effect sizes are reported as {effect_metric} "
        "({effect_scale} per Cohen, 1988)."
    )
    
    # Safe fallback for missing keys
    defaults = {
        "test_full_name": "an automated statistical pipeline",
        "version": "0.1.0",
        "citation": "StatForge Authors, 2026",
        "assumption_rationale": "Assumption checks directed the test selection.",
        "alpha": ".05",
        "effect_metric": "Cohen's d",
        "effect_scale": "interpreted"
    }
    
    kwargs = {**defaults, **pipeline_log}
    return template.format(**kwargs)
