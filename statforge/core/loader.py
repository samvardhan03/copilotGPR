import pandas as pd
import sqlite3
import tempfile
from pathlib import Path
from typing import Optional, Union
from urllib.parse import urlparse


class DataLoader:
    """Handles dynamic loading of tabular data from 15+ formats.

    Supported formats: CSV, TSV, JSON, JSONL, Excel (.xls/.xlsx),
    Parquet, Feather, SPSS (.sav), Stata (.dta), SAS (.sas7bdat/.xpt),
    HDF5 (.h5/.hdf5), SQLite (.db/.sqlite/.sqlite3), and remote URLs.

    Optional dependencies are imported lazily and produce helpful
    error messages when missing.
    """

    # Maps file extensions to internal format identifiers
    _FORMAT_MAP: dict[str, str] = {
        '.csv': 'csv',
        '.tsv': 'tsv',
        '.json': 'json',
        '.jsonl': 'jsonl',
        '.xls': 'excel',
        '.xlsx': 'excel',
        '.parquet': 'parquet',
        '.feather': 'feather',
        '.sav': 'spss',
        '.dta': 'stata',
        '.sas7bdat': 'sas',
        '.xpt': 'sas',
        '.h5': 'hdf5',
        '.hdf5': 'hdf5',
        '.db': 'sqlite',
        '.sqlite': 'sqlite',
        '.sqlite3': 'sqlite',
    }

    @staticmethod
    def detect_format(path: str) -> str:
        """Detect the file format from a path or URL without loading data.

        Args:
            path: A local file path or URL string.

        Returns:
            A format identifier string (e.g. 'csv', 'excel', 'sqlite').

        Raises:
            ValueError: If the format cannot be determined.
        """
        if path.startswith(('http://', 'https://')):
            parsed = urlparse(path)
            url_path = parsed.path.split('?')[0]
            ext = Path(url_path).suffix.lower()
            if not ext:
                raise ValueError(
                    f"Cannot detect format from URL (no file extension): {path}"
                )
        else:
            ext = Path(path).suffix.lower()

        fmt = DataLoader._FORMAT_MAP.get(ext)
        if fmt is None:
            raise ValueError(f"Unsupported file format: {ext}")
        return fmt

    @staticmethod
    def load(
        file_path: Union[str, Path],
        table: Optional[str] = None,
    ) -> pd.DataFrame:
        """Load tabular data from a file path or URL.

        Args:
            file_path: Path to a local file, or an HTTP/HTTPS URL.
            table: For SQLite files with multiple tables, specify
                   which table to load. Ignored for other formats.

        Returns:
            A pandas DataFrame containing the loaded data.

        Raises:
            FileNotFoundError: If the local file does not exist.
            ValueError: If the format is unsupported or SQLite has
                        multiple tables without a ``table`` argument.
            ImportError: If a required optional dependency is missing
                         (with install instructions in the message).
        """
        path_str = str(file_path)

        # ── URL dispatch ──────────────────────────────────────
        if path_str.startswith(('http://', 'https://')):
            return DataLoader._load_url(path_str, table=table)

        path = Path(path_str)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")

        ext = path.suffix.lower()
        fmt = DataLoader._FORMAT_MAP.get(ext)
        if fmt is None:
            raise ValueError(f"Unsupported file format: {ext}")

        return DataLoader._dispatch(fmt, path, table=table)

    # ── Private dispatch ─────────────────────────────────────

    @staticmethod
    def _dispatch(
        fmt: str,
        path: Path,
        table: Optional[str] = None,
    ) -> pd.DataFrame:
        """Route to the correct reader based on format identifier."""

        if fmt == 'csv':
            return pd.read_csv(path)

        elif fmt == 'tsv':
            return pd.read_csv(path, sep='\t')

        elif fmt == 'json':
            return pd.read_json(path)

        elif fmt == 'jsonl':
            return pd.read_json(path, lines=True)

        elif fmt == 'excel':
            try:
                import openpyxl  # noqa: F401
            except ImportError:
                raise ImportError(
                    "Loading Excel files requires openpyxl. "
                    "Install it with: pip install openpyxl"
                )
            return pd.read_excel(path)

        elif fmt == 'parquet':
            return pd.read_parquet(path)

        elif fmt == 'feather':
            try:
                import pyarrow  # noqa: F401
            except ImportError:
                raise ImportError(
                    "Loading .feather files requires pyarrow. "
                    "Install it with: pip install pyarrow"
                )
            return pd.read_feather(path)

        elif fmt == 'spss':
            try:
                import pyreadstat
            except ImportError:
                raise ImportError(
                    "Loading SPSS (.sav) files requires pyreadstat. "
                    "Install it with: pip install pyreadstat"
                )
            df, _ = pyreadstat.read_sav(str(path))
            return df

        elif fmt == 'stata':
            return pd.read_stata(path)

        elif fmt == 'sas':
            return pd.read_sas(path)

        elif fmt == 'hdf5':
            try:
                import tables  # noqa: F401
            except ImportError:
                raise ImportError(
                    "Loading HDF5 (.h5/.hdf5) files requires tables. "
                    "Install it with: pip install tables"
                )
            return pd.read_hdf(path)

        elif fmt == 'sqlite':
            return DataLoader._load_sqlite(path, table=table)

        else:
            raise ValueError(f"Unsupported file format: {fmt}")

    @staticmethod
    def _load_sqlite(
        path: Path,
        table: Optional[str] = None,
    ) -> pd.DataFrame:
        """Load data from a SQLite database file.

        If only one table exists, it is loaded automatically.
        If multiple tables exist, the ``table`` argument is required.
        """
        conn = sqlite3.connect(str(path))
        try:
            cursor = conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table'"
            )
            tables = [row[0] for row in cursor.fetchall()]

            if not tables:
                raise ValueError(f"No tables found in SQLite database: {path}")

            if table is not None:
                if table not in tables:
                    raise ValueError(
                        f"Table '{table}' not found. "
                        f"Available tables: {', '.join(tables)}"
                    )
                return pd.read_sql_query(f"SELECT * FROM \"{table}\"", conn)

            if len(tables) == 1:
                return pd.read_sql_query(
                    f"SELECT * FROM \"{tables[0]}\"", conn
                )

            raise ValueError(
                f"Multiple tables found in {path}: {', '.join(tables)}. "
                f"Specify which table to load with the table parameter, "
                f"e.g. DataLoader.load('{path}', table='{tables[0]}')"
            )
        finally:
            conn.close()

    @staticmethod
    def _load_url(
        url: str,
        table: Optional[str] = None,
    ) -> pd.DataFrame:
        """Download a remote file and load it.

        Detects the file format from the URL extension, downloads
        to a temporary file, and delegates to the standard loader.
        """
        try:
            import requests
        except ImportError:
            raise ImportError(
                "Loading files from URLs requires requests. "
                "Install it with: pip install requests"
            )

        parsed = urlparse(url)
        url_path = parsed.path.split('?')[0]
        ext = Path(url_path).suffix.lower()
        if not ext:
            raise ValueError(
                f"Cannot detect format from URL (no file extension): {url}"
            )

        response = requests.get(url, timeout=30)
        response.raise_for_status()

        with tempfile.NamedTemporaryFile(suffix=ext, delete=False) as tmp:
            tmp.write(response.content)
            tmp_path = Path(tmp.name)

        try:
            fmt = DataLoader._FORMAT_MAP.get(ext)
            if fmt is None:
                raise ValueError(f"Unsupported file format: {ext}")
            return DataLoader._dispatch(fmt, tmp_path, table=table)
        finally:
            tmp_path.unlink(missing_ok=True)
