# Getting Started

This guide provides factual, rigorous documentation on installing and running StatForge. StatForge relies on standard scientific Python stacks (pandas, scipy, PyMC) and utilizes `rich` and `questionary` for an interactive terminal experience.

## Installation

StatForge requires Python 3.10 or higher. Install the package via pip:

```bash
pip install statforge
```

## Initiating an Analysis

The primary entry point for a researcher is the `statforge run` command. 

### Interactive Wizard
If executed without explicit flags, the CLI automatically launches an interactive wizard powered by `questionary`.

```bash
statforge run my_dataset.csv
```

The wizard performs the following actions:
1.  **Data Ingestion**: Invokes the `DataLoader` to parse the provided file (supports `.csv`, `.xlsx`, `.sav`, `.parquet`).
2.  **Column Inspection**: Identifies numeric columns suitable for outcome variables.
3.  **Variable Selection**: Prompts the user to select one outcome variable and one or more grouping predictive variables.
4.  **Style Selection**: Prompts the user to select the desired output template (e.g., `apa7`).

Execution then passes to the async `run_pipeline`, rendering live progress via `rich.progress.Progress`.

## Validating Data Quality

Before executing complex Bayesian models, researchers should use the `validate` command. This performs preliminary checks on the dataset structure entirely decoupled from the statistical models.

```bash
statforge validate my_dataset.csv
```

The sequence includes:
*   Checking for missing values (flagging columns >20% missing).
*   Flagging data type anomalies (e.g., numeric vectors encoded as strings).
*   Screening for severe outliers utilizing standard IQR methodologies.

## Configuration Scaffold

To generate a reproducible configuration scaffold within your working directory, execute:

```bash
statforge config
```

This outputs a `statforge_config.yaml` defining global parameters (e.g., `random_seed`, `default_priority`, `alpha`).
