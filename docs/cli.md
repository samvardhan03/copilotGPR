# CLI Reference

The StatForge CLI acts as the primary orchestrator for the execution pipeline. It provides four distinct commands.

## statforge run

Executes the full six-stage analytical pipeline: `DataLoader` $\rightarrow$ `AssumptionChecker` $\rightarrow$ `MethodSelector` $\rightarrow$ `ModelFitter` $\rightarrow$ `ResultFormatter` $\rightarrow$ `ReportBuilder`.

**Usage:**
```bash
statforge run <data_file_path>
```

If `<data_file_path>` is provided without additional flags, the interactive wizard is launched to guide variable selection.

## statforge validate

Provides a rigorous preliminary assessment of dataset quality to ensure stability during the `ModelFitter` stage.

**Usage:**
```bash
statforge validate <data_file_path>
```

Execution terminates with an exit code of `1` if critical structural issues (e.g., unparseable encodings) are detected, ensuring CI/CD compatibility.

## statforge chat

*Note: The LangChain conversational agent is an exploratory wrapper and currently routes strictly through the predefined CLI capabilities.*

**Usage:**
```bash
statforge chat
```

## statforge config

Emits the default runtime configuration tree to `statforge_config.yaml` for modification and reproducible pipeline executions.

**Usage:**
```bash
statforge config
```
