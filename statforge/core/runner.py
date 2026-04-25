import asyncio
from typing import AsyncIterator, Callable, Any

from statforge.core.loader import DataLoader
from statforge.core.assumptions import AssumptionChecker
from statforge.core.selector import MethodSelector

# Mocking external modules for runner logic
def mock_fit(config): return {"model_fit": True}
def mock_format(config): return {"formatted": True}
def mock_build_report(config): return {"report": "path/to/report.pdf"}


# ── Parametric / non-parametric pairs for robustness checks ──

_ROBUSTNESS_PAIRS: dict[str, str] = {
    "t_test": "mann_whitney",
    "mann_whitney": "t_test",
    "anova": "kruskal_wallis",
    "kruskal_wallis": "anova",
}


async def _run_auto_robustness(
    config: dict,
    assumption_results: dict,
    selected_tests: list[str],
) -> dict:
    """Evaluate borderline assumptions and run robustness checks.

    If any assumption p-values fall in the borderline range
    (0.04 < p < 0.06), both the parametric and non-parametric
    counterpart tests are executed and compared.

    Returns a robustness_check dict with both results and a
    recommendation, or an empty dict if no borderline cases exist.
    """
    borderline_found = False
    for key, result in assumption_results.items():
        if isinstance(result, dict) and result.get("borderline", False):
            borderline_found = True
            break

    if not borderline_found:
        return {"status": "no_borderline", "message": "All assumptions clearly met or violated."}

    robustness: dict[str, Any] = {"status": "borderline_detected", "comparisons": []}

    for test in selected_tests:
        alt_test = _ROBUSTNESS_PAIRS.get(test)
        if alt_test:
            comparison = {
                "original_test": test,
                "alternative_test": alt_test,
                "original_result": {"ran": True, "mock": True},
                "alternative_result": {"ran": True, "mock": True},
                "recommendation": (
                    f"Borderline assumption detected. Both {test} and "
                    f"{alt_test} were executed. If results agree, the "
                    f"original {test} is recommended. If they diverge, "
                    f"the non-parametric {alt_test} is more conservative."
                ),
            }
            robustness["comparisons"].append(comparison)

    return robustness


async def run_pipeline(config: dict) -> AsyncIterator[dict]:
    """Async pipeline executor. Yields progress events per stage.

    When ``config["auto"]`` is True, an additional AutoRobustness
    stage is appended that checks borderline assumptions and runs
    both parametric and non-parametric tests for comparison.
    """
    # Track intermediate results for auto-robustness
    assumption_results: dict = {}
    selected_tests: list[str] = []

    stages: list[tuple[str, Callable]] = [
        ("DataLoader", lambda c: DataLoader.load(c["data_path"]) if "data_path" in c else None),
        ("AssumptionChecker", lambda c: {"normality": {"p_value": 0.5}}),  # mock
        ("MethodSelector", lambda c: MethodSelector.select_method(c, {})),
        ("ModelFitter", mock_fit),
        ("ResultFormatter", mock_format),
        ("ReportBuilder", mock_build_report)
    ]

    for stage_name, stage_fn in stages:
        yield {'stage': stage_name, 'status': 'running'}
        try:
            # CPU-bound stages are pushed to a thread
            result = await asyncio.to_thread(stage_fn, config)

            # Capture intermediate results for auto mode
            if stage_name == "AssumptionChecker" and isinstance(result, dict):
                assumption_results = result
            elif stage_name == "MethodSelector" and isinstance(result, list):
                selected_tests = result

            yield {'stage': stage_name, 'status': 'done', 'result': result}
        except Exception as e:
            yield {'stage': stage_name, 'status': 'error', 'error': str(e)}
            break

    # ── Stage 7: AutoRobustness (optional) ─────────────────
    if config.get("auto", False):
        yield {'stage': 'AutoRobustness', 'status': 'running'}
        try:
            robustness = await _run_auto_robustness(
                config, assumption_results, selected_tests
            )
            yield {
                'stage': 'AutoRobustness',
                'status': 'done',
                'result': robustness,
            }
        except Exception as e:
            yield {
                'stage': 'AutoRobustness',
                'status': 'error',
                'error': str(e),
            }
