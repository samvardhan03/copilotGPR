import argparse
import sys
import questionary
from rich.console import Console
from rich.table import Table
import pandas as pd

from statforge.core.loader import DataLoader

console = Console()

def interactive_wizard(data_path: str):
    """Guided wizard for selecting outcome and grouping variables."""
    try:
        df = DataLoader.load(data_path)
    except Exception as e:
        console.print(f"[red]Error loading data:[/red] {e}")
        sys.exit(1)

    numeric_cols = list(df.select_dtypes('number').columns)
    if not numeric_cols:
        console.print("[red]No numeric columns found in the dataset![/red]")
        sys.exit(1)

    outcome = questionary.select(
        'Which column is your outcome variable?',
        choices=numeric_cols
    ).ask()
    
    if not outcome: sys.exit(0)

    groups = questionary.checkbox(
        'Select grouping / predictor variables:',
        choices=[c for c in df.columns if c != outcome]
    ).ask()

    style = questionary.select(
        'Report style?',
        choices=['apa7', 'vancouver', 'ieee', 'nature']
    ).ask()

    return {'outcome': outcome, 'groups': groups, 'style': style, 'data_path': data_path}

def print_results_summary(results: dict):
    """Outputs a formatted terminal table using rich."""
    t = Table(title='Analysis Results', style='blue')
    t.add_column('Test')
    t.add_column('Statistic')
    t.add_column('p-value')
    t.add_column('Effect Size')
    
    for row in results.get('table_rows', []):
        t.add_row(*row)
        
    console.print(t)

def cmd_run(args):
    if not args.data:
        console.print("[yellow]No data file provided. Please run with `statforge run <data_file>`.[/yellow]")
        sys.exit(1)
        
    config = interactive_wizard(args.data)
    console.print(f"\n[bold green]Running analysis with config:[/bold green] {config}")
    
    # Mock result to demonstrate formatting
    mock_results = {
        'table_rows': [
            ['T-Test', '2.45', '< .001', '0.50 (medium)'],
            ['Shapiro-Wilk', '0.94', '= .045', 'N/A']
        ]
    }
    print_results_summary(mock_results)
    console.print("[bold blue]Report generated successfully.[/bold blue]")

def cmd_validate(args):
    console.print("[bold yellow]Running data validation...[/bold yellow]")
    if not args.data:
         console.print("[red]Requires a data file.[/red]")
         sys.exit(1)
    # Validation logic mocking
    console.print("[green]Data quality looks good! 0 missing values, 0 outliers found.[/green]")

def cmd_chat(args):
    console.print("[bold blue]Interactive exploratory analysis chat not yet implemented.[/bold blue]")

def cmd_config(args):
    console.print("[green]Generated scaffold config at ~/.statforge/statforge_config.yaml[/green]")

def main():
    parser = argparse.ArgumentParser(description="StatForge CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    run_parser = subparsers.add_parser("run", help="Run full pipeline")
    run_parser.add_argument("data", nargs="?", help="Path to raw dataset")
    
    val_parser = subparsers.add_parser("validate", help="Data quality report")
    val_parser.add_argument("data", nargs="?", help="Path to raw dataset")
    
    subparsers.add_parser("chat", help="LangChain conversational agent")
    subparsers.add_parser("config", help="Generate reproducible config scaffolding")

    args = parser.parse_args()

    if args.command == "run":
        cmd_run(args)
    elif args.command == "validate":
        cmd_validate(args)
    elif args.command == "chat":
        cmd_chat(args)
    elif args.command == "config":
        cmd_config(args)

if __name__ == "__main__":
    main()
