import argparse
from api_client import DeepSeekClient
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich import print as rprint


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="DeepSeek AI Chat with Markdown Output"
    )
    parser.add_argument("question", nargs="*", help="Input question for AI")
    parser.add_argument("--model", "-m", type=str, default=None, help="Model name")

    args = parser.parse_args()

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

        # 默认中文回答
        question += " (请用中文回答我的问题，但是如果我的需求是翻译，则不需要强制中文)"

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
