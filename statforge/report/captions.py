def generate_caption(fig_type: str, analysis_meta: dict, fig_number: int = 1) -> str:
    """Generates an APA-compliant caption for figures based on their type."""
    templates = {
        'distribution': 'Figure {n}. Distribution of {outcome} by {group} '
                        'with individual data points and median (horizontal bar).',
        'boxplot': 'Figure {n}. Box plots of {outcome} across {group} '
                   'conditions. Whiskers extend to 1.5 x IQR.',
        'regression': 'Figure {n}. Scatter plot of {outcome} and {predictor} '
                      'with fitted regression line (95% CI shaded).'
    }
    
    template = templates.get(fig_type, 'Figure {n}. General plot of {outcome}.')
    return template.format(n=fig_number, **analysis_meta)
