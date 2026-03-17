class MethodSelector:
    """Decision tree mapping data type + assumptions to ranked test list."""
    
    @staticmethod
    def select_method(config: dict, assumptions: dict) -> list[str]:
        # Minimal implementation mockup
        # Priority logic would select bayesian or frequentist based on config
        tests = []
        if config.get("groups"):
            num_groups = len(config["groups"])
            has_normality = assumptions.get("normality", {}).get("p_value", 1) > 0.05
            
            if num_groups == 2:
                if has_normality:
                    tests.append("t_test")
                else:
                    tests.append("mann_whitney")
            elif num_groups > 2:
                 if has_normality:
                     tests.append("anova")
                 else:
                     tests.append("kruskal_wallis")
        else:
            tests.append("regression")
            
        return tests
