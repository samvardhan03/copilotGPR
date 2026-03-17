
# StatForge

**Automated Bayesian-frequentist statistics and publication-ready reports.**

![StatForge Demo](demo.gif)

StatForge is an open-source Python library and command-line interface designed to automate statistical analysis and generate publication-ready reports. Built for academic researchers, biostatisticians, and data scientists, StatForge streamlines the process from raw data ingestion to formatted output (PDF, DOCX, HTML).

## Overview

StatForge implements a robust six-stage execution pipeline:
1.  **DataLoader**: Ingests data from CSV, Excel, SPSS (.sav), and Parquet formats.
2.  **AssumptionChecker**: Performs statistical assumption checks (e.g., normality, homoscedasticity) utilizing a SHA-256 keyed caching layer (`joblib.Memory`) for optimized iterative checks.
3.  **MethodSelector**: Automatically ranks and selects appropriate tests based on data characteristics and assumption results.
4.  **ModelFitter**: Dispatches analysis to a plugin registry supporting both frequentist methods (SciPy, statsmodels) and Bayesian inference (PyMC).
5.  **ResultFormatter**: Structures statistical output including effect sizes for standardized reporting.
6.  **ReportBuilder**: Orchestrates the final document utilizing Jinja2 templates, generating APA or Vancouver styled tables, automated methods summaries, and figure captions.

## Installation

```bash
pip install statforge
```

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

### 2. Validating Data Quality

Before running a full analysis, generate a data quality report to flag missing values, outliers, or type mismatches:

```bash
statforge validate dataset.csv
```

### 3. Generating a Configuration File

For reproducible analyses, generate a configuration scaffold:

```bash
statforge config
```

This creates a `statforge_config.yaml` file that you can customize and version control.

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


