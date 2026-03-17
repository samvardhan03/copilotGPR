class ResultFormatter:
    """Formats model results into APA/Vancouver compliant tables and summaries."""
    
    @staticmethod
    def format_apa(results: dict) -> dict:
        """Formats the result dictionary for APA7 standard output."""
        table_rows = []
        for res in results.get("tests", []):
            test_name = res.get("name")
            stat = f"{res.get('stat_value'):.2f}"
            p_val = res.get("p_value")
            p_str = "< .001" if p_val < 0.001 else f"= {p_val:.3f}".replace("0.", ".", 1)
            effect = res.get("effect_size", {})
            effect_str = f"{effect.get('value', 0):.2f} ({effect.get('label', '')})"
            
            table_rows.append([test_name, stat, p_str, effect_str])
            
        return {"table_rows": table_rows}
