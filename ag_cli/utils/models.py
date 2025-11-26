# utils/models.py
from rich.console import Console
from rich.table import Table
from ag_cli.config import load_config


def list_models():
    """列出所有支持的模型代称和实际名称"""
    config = load_config()
    model_mapping = config["model_mapping"]

    console = Console()
    table = Table(title="支持的模型代称", show_header=True, header_style="bold magenta")
    table.add_column("代称", style="cyan", width=10)
    table.add_column("实际模型名称", style="green")

    for alias, actual_name in model_mapping.items():
        table.add_row(alias, actual_name)

    console.print(table)
