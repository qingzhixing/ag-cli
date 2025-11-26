import argparse
from api_client import DeepSeekClient
from config import load_config
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.table import Table
from rich import print as rprint


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


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="DeepSeek AI Chat with Markdown Output"
    )
    parser.add_argument("question", nargs="*", help="Input question for AI")
    parser.add_argument(
        "--model", "-m", type=str, default=None, help="Model name or alias"
    )
    parser.add_argument(
        "--list-models",
        "-l",
        action="store_true",
        help="List all supported model aliases",
    )

    args = parser.parse_args()

    # 如果请求列出模型，则显示模型列表并退出
    if args.list_models:
        list_models()
        return

    # 获取问题
    if args.question:
        question = " ".join(args.question)
    else:
        question = input("请输入您的问题: ")

    if not question.strip():
        rprint("[red]问题不能为空！[/red]")
        return

    # 初始化客户端和控制台
    client = DeepSeekClient()
    console = Console()

    try:
        # 显示问题
        console.print(
            Panel.fit(
                f"[bold cyan]{question}[/bold cyan]",
                title="[bold blue]问题[/bold blue]",
                border_style="blue",
            )
        )

        # 显示加载状态
        with console.status("[bold green]思考中...", spinner="dots"):
            # 获取完整响应
            response = client.chat(question, model=args.model)

        # 显示回答
        console.print("\n[bold green]回答:[/bold green]\n")

        if response is None:
            console.print("[yellow]模型返回了空响应。[/yellow]")

        else:
            # 使用 Rich 的 Markdown 渲染响应
            markdown = Markdown(response)
            console.print(markdown)

    except Exception as e:
        console.print(f"[red]错误: {str(e)}[/red]")


if __name__ == "__main__":
    main()
