"""Interactive Data Analyst Chat — microgpt-inspired REPL.

Implements Karpathy's microgpt philosophy: treat any corpus as
``docs: list[str]`` and everything else is just efficiency.

Each row of the user's dataset becomes a natural-language document.
Questions are answered via keyword-overlap retrieval over these
documents, with optional LLM augmentation via the Anthropic API.
"""

import asyncio
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Optional

import pandas as pd
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.table import Table

from statforge.core.loader import DataLoader

console = Console()


class DataAnalyst:
    """Interactive data analyst REPL for tabular datasets.

    Args:
        data_path: Path to a dataset file (any format supported by DataLoader).
        table: Optional table name for SQLite files.
    """

    def __init__(self, data_path: str, table: Optional[str] = None) -> None:
        self.data_path = data_path
        self.df: pd.DataFrame = DataLoader.load(data_path, table=table)
        self.docs: list[str] = self._build_docs(self.df)
        self.summary: str = self._build_summary(self.df)
        self.history: list[dict[str, str]] = []
        self._has_api_key = bool(os.environ.get("ANTHROPIC_API_KEY"))

    # ── Document construction (microgpt-style) ──────────────

    @staticmethod
    def _build_docs(df: pd.DataFrame) -> list[str]:
        """Convert each row into a natural-language document string.

        Following microgpt philosophy: represent the entire dataset
        as ``docs: list[str]`` where each element is a row.
        """
        docs: list[str] = []
        cols = list(df.columns)
        for i, row in df.iterrows():
            parts = [f"{col}={row[col]}" for col in cols]
            docs.append(f"Row {i}: {', '.join(parts)}")
        return docs

    @staticmethod
    def _build_summary(df: pd.DataFrame) -> str:
        """Compute dataset-level summary statistics as a context block."""
        lines: list[str] = []
        lines.append(f"Dataset: {df.shape[0]} rows × {df.shape[1]} columns")
        lines.append(f"Columns: {', '.join(df.columns)}")
        lines.append(f"Dtypes: {dict(df.dtypes.value_counts())}")
        lines.append(f"Null counts: {dict(df.isnull().sum())}")

        numeric = df.select_dtypes("number")
        if not numeric.empty:
            lines.append("\nNumeric summary:")
            for col in numeric.columns:
                s = numeric[col]
                lines.append(
                    f"  {col}: mean={s.mean():.4f}, std={s.std():.4f}, "
                    f"min={s.min():.4f}, max={s.max():.4f}, "
                    f"nulls={s.isnull().sum()}"
                )
        return "\n".join(lines)

    # ── Retrieval ────────────────────────────────────────────

    def _retrieve_relevant_rows(self, query: str, k: int = 10) -> list[str]:
        """Return the top-k most relevant row-documents by keyword overlap.

        Tokenizes the query and scores each document by the number
        of overlapping words (case-insensitive).
        """
        query_tokens = set(re.findall(r'\w+', query.lower()))
        scored: list[tuple[int, str]] = []
        for doc in self.docs:
            doc_tokens = set(re.findall(r'\w+', doc.lower()))
            overlap = len(query_tokens & doc_tokens)
            scored.append((overlap, doc))
        scored.sort(key=lambda x: x[0], reverse=True)
        return [doc for _, doc in scored[:k]]

    # ── Context assembly ─────────────────────────────────────

    def _build_context(self, query: str) -> str:
        """Assemble the context window for an LLM or rule-based response.

        Includes: dataset summary, top-k relevant rows, and the
        last 5 conversation turns.
        """
        relevant = self._retrieve_relevant_rows(query)
        parts: list[str] = []

        parts.append("=== DATASET SUMMARY ===")
        parts.append(self.summary)

        parts.append("\n=== RELEVANT ROWS ===")
        parts.extend(relevant)

        if self.history:
            parts.append("\n=== CONVERSATION HISTORY ===")
            for turn in self.history[-5:]:
                parts.append(f"User: {turn['user']}")
                parts.append(f"Assistant: {turn['assistant']}")

        return "\n".join(parts)

    # ── LLM / fallback ───────────────────────────────────────

    def _call_llm(self, query: str) -> str:
        """Send query + context to Anthropic API, or fall back to rules."""
        if not self._has_api_key:
            return self._rule_based_respond(query)

        try:
            import anthropic
        except ImportError:
            return self._rule_based_respond(query)

        context = self._build_context(query)
        system_prompt = (
            "You are a data analyst assistant for a tabular dataset loaded "
            "in StatForge. Answer questions about the data precisely and "
            "concisely. Use the provided dataset summary and relevant rows "
            "to inform your answers. If you are uncertain, say so."
        )

        client = anthropic.Anthropic()
        message = client.messages.create(
            model="claude-sonnet-4-6-20250514",
            max_tokens=1024,
            system=system_prompt,
            messages=[
                {"role": "user", "content": f"{context}\n\nQuestion: {query}"}
            ],
        )
        return message.content[0].text

    def _rule_based_respond(self, query: str) -> str:
        """Simple rule-based responder when no API key is available."""
        q = query.lower().strip()

        # Column-specific stat queries
        for col in self.df.columns:
            if col.lower() in q:
                if "mean" in q or "average" in q:
                    if self.df[col].dtype in ("float64", "int64"):
                        return f"The mean of '{col}' is {self.df[col].mean():.4f}"
                if "max" in q or "maximum" in q:
                    return f"The max of '{col}' is {self.df[col].max()}"
                if "min" in q or "minimum" in q:
                    return f"The min of '{col}' is {self.df[col].min()}"
                if "std" in q or "deviation" in q:
                    if self.df[col].dtype in ("float64", "int64"):
                        return f"The std dev of '{col}' is {self.df[col].std():.4f}"

        if "how many rows" in q or "row count" in q:
            return f"The dataset has {len(self.df)} rows."

        if "how many columns" in q or "column count" in q:
            return f"The dataset has {len(self.df.columns)} columns: {', '.join(self.df.columns)}"

        if "columns" in q or "fields" in q:
            return f"Columns: {', '.join(self.df.columns)}"

        if "shape" in q or "size" in q:
            return f"Dataset shape: {self.df.shape[0]} rows × {self.df.shape[1]} columns"

        return (
            "I can answer basic questions about columns, means, min/max, "
            "and row counts. For advanced analysis, set the ANTHROPIC_API_KEY "
            "environment variable or use `/analyze` to run the full pipeline."
        )

    # ── Special commands ─────────────────────────────────────

    def _cmd_describe(self) -> None:
        """Display full dataset profile."""
        console.print(Panel("[bold]Dataset Profile[/bold]", style="blue"))
        console.print(self.summary)
        console.print()

        desc = self.df.describe(include="all").to_string()
        console.print(Panel(desc, title="df.describe()", style="dim"))

    def _cmd_analyze(self) -> None:
        """Trigger full StatForge pipeline on the current dataset."""
        console.print(
            "[bold yellow]Running full StatForge pipeline...[/bold yellow]"
        )
        from statforge.core.runner import run_pipeline

        config = {"data_path": self.data_path, "auto": False}

        async def _run() -> None:
            async for event in run_pipeline(config):
                stage = event.get("stage", "")
                status = event.get("status", "")
                if status == "done":
                    console.print(f"  [green]✔[/green] {stage}")
                elif status == "error":
                    console.print(
                        f"  [red]✘[/red] {stage}: {event.get('error')}"
                    )

        asyncio.run(_run())
        console.print("[bold green]Pipeline complete.[/bold green]")

    def _cmd_export(self) -> None:
        """Save conversation history to a Markdown file."""
        if not self.history:
            console.print("[yellow]No conversation to export.[/yellow]")
            return

        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        out_path = Path(f"statforge_chat_{ts}.md")
        lines: list[str] = [f"# StatForge Chat Export — {ts}\n"]
        lines.append(f"**Dataset:** `{self.data_path}`\n")
        for turn in self.history:
            lines.append(f"**You:** {turn['user']}\n")
            lines.append(f"**StatForge:** {turn['assistant']}\n")
            lines.append("---\n")

        out_path.write_text("\n".join(lines))
        console.print(
            f"[green]Conversation exported to {out_path}[/green]"
        )

    # ── Main REPL loop ───────────────────────────────────────

    def run(self) -> None:
        """Start the interactive data analyst REPL."""
        console.print(
            Panel(
                "[bold]StatForge Data Analyst[/bold]\n"
                f"Loaded [cyan]{self.data_path}[/cyan] — "
                f"{self.df.shape[0]} rows × {self.df.shape[1]} columns\n\n"
                "Commands: [dim]/describe  /analyze  /export  /quit[/dim]",
                style="blue",
                padding=(1, 2),
            )
        )

        if not self._has_api_key:
            console.print(
                "[dim]Tip: Set ANTHROPIC_API_KEY for AI-powered answers. "
                "Currently using rule-based mode.[/dim]\n"
            )

        while True:
            try:
                query = input("you › ").strip()
            except (EOFError, KeyboardInterrupt):
                console.print("\n[dim]Goodbye.[/dim]")
                break

            if not query:
                continue

            if query.lower() in ("/quit", "/exit", "/q"):
                console.print("[dim]Goodbye.[/dim]")
                break
            elif query.lower() == "/describe":
                self._cmd_describe()
                continue
            elif query.lower() == "/analyze":
                self._cmd_analyze()
                continue
            elif query.lower() == "/export":
                self._cmd_export()
                continue

            response = self._call_llm(query)
            self.history.append({"user": query, "assistant": response})

            console.print()
            console.print(Markdown(response))
            console.print()
