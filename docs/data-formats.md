# Supported Data Formats

StatForge's `DataLoader` supports a wide range of tabular data formats. Formats requiring optional dependencies will produce a clear error message with install instructions if the dependency is missing.

## Format Reference

| Extension(s)                 | Format      | Reader                        | Optional Dependency   | Install Command              |
|------------------------------|-------------|-------------------------------|-----------------------|------------------------------|
| `.csv`                       | CSV         | `pd.read_csv`                 | —                     | —                            |
| `.tsv`                       | TSV         | `pd.read_csv(sep='\t')`       | —                     | —                            |
| `.json`                      | JSON        | `pd.read_json`                | —                     | —                            |
| `.jsonl`                     | JSON Lines  | `pd.read_json(lines=True)`    | —                     | —                            |
| `.xls`, `.xlsx`              | Excel       | `pd.read_excel`               | openpyxl              | `pip install statforge[excel]` |
| `.parquet`                   | Parquet     | `pd.read_parquet`             | pyarrow / fastparquet | `pip install statforge[parquet]` |
| `.feather`                   | Feather     | `pd.read_feather`             | pyarrow               | `pip install statforge[parquet]` |
| `.sav`                       | SPSS        | `pyreadstat.read_sav`         | pyreadstat            | `pip install statforge[spss]`  |
| `.dta`                       | Stata       | `pd.read_stata`               | —                     | —                            |
| `.sas7bdat`, `.xpt`          | SAS         | `pd.read_sas`                 | —                     | —                            |
| `.h5`, `.hdf5`               | HDF5        | `pd.read_hdf`                 | tables                | `pip install statforge[hdf]`   |
| `.db`, `.sqlite`, `.sqlite3` | SQLite      | `sqlite3 + pd.read_sql_query` | —                     | —                            |
| URL (`http://`, `https://`)  | Remote file | Auto-detect from URL          | requests              | `pip install statforge[full]`  |

## Installing All Format Support

To install StatForge with all optional dependencies:

```bash
pip install statforge[full]
```

## Usage Examples

### Loading a CSV file
```python
from statforge.core.loader import DataLoader

df = DataLoader.load("experiment_data.csv")
```

### Loading an Excel file
```python
df = DataLoader.load("results.xlsx")
```

### Loading from a URL
```python
df = DataLoader.load("https://example.com/data/survey.csv")
```

### Loading a SQLite database
```python
# Auto-loads if only one table exists
df = DataLoader.load("research.db")

# Specify a table name explicitly
df = DataLoader.load("research.db", table="participants")
```

### Detecting format without loading
```python
fmt = DataLoader.detect_format("data.parquet")
# Returns: "parquet"
```

## CLI Usage

All supported formats work directly with the CLI:

```bash
statforge run experiment.csv
statforge run results.xlsx
statforge run survey.sav
statforge run database.sqlite
statforge chat measurements.parquet
```
