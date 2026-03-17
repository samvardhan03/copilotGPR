import asyncio
from typing import AsyncIterator, Callable, Any

from statforge.core.loader import DataLoader
from statforge.core.assumptions import AssumptionChecker
from statforge.core.selector import MethodSelector

# Mocking external modules for runner logic
def mock_fit(config): return {"model_fit": True}
def mock_format(config): return {"formatted": True}
def mock_build_report(config): return {"report": "path/to/report.pdf"}

async def run_pipeline(config: dict) -> AsyncIterator[dict]:
    """
    Async pipeline executor. Yields progress events per stage.
    """
    stages: list[tuple[str, Callable]] = [
        ("DataLoader", lambda c: DataLoader.load(c["data_path"]) if "data_path" in c else None),
        ("AssumptionChecker", lambda c: {"normality": {"p_value": 0.5}}), # mock
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
            yield {'stage': stage_name, 'status': 'done', 'result': result}
        except Exception as e:
            yield {'stage': stage_name, 'status': 'error', 'error': str(e)}
            break
