
# StatForge

[![PyPI version](https://img.shields.io/pypi/v/statforge)](https://pypi.org/project/statforge/)
[![PyPI downloads](https://img.shields.io/pypi/dm/statforge)](https://pypi.org/project/statforge/)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)

**Automated Bayesian-frequentist statistics and publication-ready reports.**

StatForge is an open-source Python library and command-line interface designed to automate statistical analysis and generate publication-ready reports. Built for academic researchers, biostatisticians, and data scientists, StatForge streamlines the process from raw data ingestion to formatted output (PDF, DOCX, HTML).

## Installation

```bash
pip install statforge[full]
```

This installs all optional dependencies for maximum format support. For a minimal install:

```bash
pip install statforge
```

## Overview

StatForge implements a robust six-stage execution pipeline with an optional seventh autonomous robustness stage:

1.  **DataLoader**: Ingests data from 15+ formats — CSV, TSV, JSON, Excel, Parquet, Feather, SPSS (.sav), Stata (.dta), SAS, HDF5, SQLite, and remote URLs.
2.  **AssumptionChecker**: Performs statistical assumption checks (e.g., normality, homoscedasticity) utilizing a SHA-256 keyed caching layer (`joblib.Memory`) for optimized iterative checks.
3.  **MethodSelector**: Automatically ranks and selects appropriate tests based on data characteristics and assumption results.
4.  **ModelFitter**: Dispatches analysis to a plugin registry supporting both frequentist methods (SciPy, statsmodels) and Bayesian inference (PyMC).
5.  **ResultFormatter**: Structures statistical output including effect sizes for standardized reporting.
6.  **ReportBuilder**: Orchestrates the final document utilizing Jinja2 templates, generating APA or Vancouver styled tables, automated methods summaries, and figure captions.
7.  **AutoRobustness** *(optional)*: When `--auto` is enabled, automatically detects borderline assumptions and runs both parametric and non-parametric counterpart tests for comparison.

## Quick Start

### 1. Interactive CLI Wizard

The easiest way to begin an analysis is via the interactive wizard. Navigate to your dataset and execute:

```bash
statforge run dataset.csv
```

The wizard will prompt you to:
*   Select the outcome variable.
*   Select grouping or predictor variables.
*   Choose a report style (e.g., APA7).

### 2. Autonomous Robustness Mode

Enable automatic robustness checks for borderline assumptions:

```bash
statforge run dataset.csv --auto
```

When borderline p-values (0.04 < p < 0.06) are detected, StatForge automatically runs both parametric and non-parametric tests and compares results.

### 3. Interactive Data Analyst Chat

Explore your dataset interactively using AI-powered analysis:

```bash
statforge chat dataset.csv
```

Commands: `/describe` (full profile), `/analyze` (run pipeline), `/export` (save conversation), `/quit`.

Set `ANTHROPIC_API_KEY` for AI-powered answers, or use the built-in rule-based mode.

### 4. Validating Data Quality

Before running a full analysis, generate a data quality report to flag missing values, outliers, or type mismatches:

```bash
statforge validate dataset.csv
```

### 5. Generating a Configuration File

For reproducible analyses, generate a configuration scaffold:

```bash
statforge config
```

This creates a `statforge_config.yaml` file that you can customize and version control.

## Supported Data Formats

| Format     | Extensions                    | Optional Dependency |
|------------|-------------------------------|---------------------|
| CSV        | `.csv`                        | —                   |
| TSV        | `.tsv`                        | —                   |
| JSON/JSONL | `.json`, `.jsonl`             | —                   |
| Excel      | `.xls`, `.xlsx`               | openpyxl            |
| Parquet    | `.parquet`                    | pyarrow             |
| Feather    | `.feather`                    | pyarrow             |
| SPSS       | `.sav`                        | pyreadstat          |
| Stata      | `.dta`                        | —                   |
| SAS        | `.sas7bdat`, `.xpt`           | —                   |
| HDF5       | `.h5`, `.hdf5`                | tables              |
| SQLite     | `.db`, `.sqlite`, `.sqlite3`  | —                   |
| URL        | `http://`, `https://`         | requests            |

Install specific format support: `pip install statforge[excel]`, `statforge[spss]`, etc.

## Bayesian Analysis & PriorAdvisor

StatForge lowers the barrier to Bayesian analysis through its `PriorAdvisor` module. 

*   **Guided Priors**: `PriorAdvisor` suggests data-driven, weakly informative priors (e.g., assigning a Normal distribution with $\mu$ equal to the observed mean and $\sigma$ equal to twice the observed standard deviation). 
*   **Transparency**: The rationale for the selected priors is clearly documented and included in the generated report's methodology section.
*   **Sensitivity Analysis**: The pipeline automatically evaluates posterior stability across weakly informative, uninformative, and highly informative prior variants to ensure robustness.

## Model Plugin Registry

StatForge utilizes a `@register` decorator pattern, allowing seamless integration of custom analytical models. Users can drop custom `.py` model definitions directly into `~/.statforge/plugins/`, and they will be dynamically loaded by the pipeline. See `CONTRIBUTING.md` for details on writing custom plugins.

## Cite StatForge

If you use StatForge in your research, please cite our JOSS paper (DOI pending). See `paper/paper.md` and `paper/paper.bib` for citation details.

---

Made by **Samvardhan Singh**. Licensed under the Apache License 2.0.
