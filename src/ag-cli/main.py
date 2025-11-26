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


def manage_context(conversation_history, max_tokens=120000):
    """
    管理对话上下文，防止超过模型限制
    简单的实现：保留最近N轮对话
    """
    # 如果对话历史太长，保留最近的对话
    if len(conversation_history) > 20:  # 保留最近10轮对话（20条消息）
        # 保留系统消息和最近的对话
        system_msg = conversation_history[0]  # 系统消息
        recent_history = conversation_history[-18:]  # 最近9轮对话
        return [system_msg] + recent_history
    return conversation_history


def continuous_chat(client, console, model=None):
    """连续对话模式"""
    conversation_history = []

    # 添加系统提示，要求默认使用中文
    system_prompt = "请使用中文进行回答。"
    conversation_history.append({"role": "system", "content": system_prompt})

    console.print("[bold green]进入连续对话模式[/bold green]")
    console.print("[dim]输入 '.' 单独一行结束多行输入[/dim]")
    console.print("[dim]输入 '.exit' 结束对话[/dim]")
    console.print("[dim]输入 '.clear' 清空对话历史[/dim]")
    console.print("[dim]输入 '.history' 查看对话历史[/dim]\n")

    while True:
        try:
            # 获取用户输入
            console.print("[bold cyan]您:[/bold cyan] ")
            lines = []
            while True:
                try:
                    line = input()
                    # 检查特殊命令
                    if line.strip() == ".exit":
                        console.print("[yellow]结束对话。[/yellow]")
                        return
                    elif line.strip() == ".clear":
                        conversation_history = [
                            {"role": "system", "content": "请使用中文进行回答。"}
                        ]
                        console.print("[green]对话历史已清空。[/green]")
                        break
                    elif line.strip() == ".history":
                        console.print("\n[bold yellow]对话历史:[/bold yellow]")
                        for i, msg in enumerate(
                            conversation_history[1:], 1
                        ):  # 跳过系统消息
                            role = "用户" if msg["role"] == "user" else "AI"
                            content_preview = (
                                msg["content"][:100] + "..."
                                if len(msg["content"]) > 100
                                else msg["content"]
                            )
                            console.print(f"  {i}. {role}: {content_preview}")
                        console.print()
                        break
                    elif line.strip() == ".":
                        break
                    lines.append(line)
                except EOFError:
                    break

            # 如果没有实际内容，继续循环
            if not lines and not any(
                cmd in [".clear", ".history"]
                for cmd in [line.strip() for line in lines if line.strip()]
            ):
                continue

            # 构建用户输入
            user_input = "\n".join(lines)

            # 跳过空输入
            if not user_input.strip():
                continue

            # 添加到对话历史
            conversation_history.append({"role": "user", "content": user_input})

            try:
                # 管理上下文长度
                managed_history = manage_context(conversation_history)

                # 显示加载状态
                with console.status("[bold green]思考中...", spinner="dots"):
                    # 调用API
                    response = client.chat_completion(managed_history, model=model)

                # 显示回答
                console.print("\n[bold green]AI:[/bold green]")

                if response is None:
                    console.print("[yellow]模型返回了空响应。[/yellow]")
                else:
                    # 使用 Rich 的 Markdown 渲染响应
                    markdown = Markdown(response)
                    console.print(markdown)
                    console.print()  # 空行

                    # 将AI回复添加到对话历史
                    conversation_history.append(
                        {"role": "assistant", "content": response}
                    )

            except Exception as e:
                console.print(f"[red]API调用错误: {str(e)}[/red]")
                # 移除最后一条用户消息，因为处理失败了
                if conversation_history and conversation_history[-1]["role"] == "user":
                    conversation_history.pop()

        except KeyboardInterrupt:
            console.print("\n[yellow]结束对话。[/yellow]")
            break


def single_chat(client, console, question, model=None):
    """单次对话模式"""
    try:
        # 显示问题
        console.print(
            Panel.fit(
                f"[bold cyan]{question}[/bold cyan]",
                title="[bold blue]问题[/bold blue]",
                border_style="blue",
            )
        )

        # 添加语言提示
        question_with_lang = question + " (当我未指定语言时，默认使用中文进行回答)"

        # 显示加载状态
        with console.status("[bold green]思考中...", spinner="dots"):
            # 获取完整响应
            response = client.chat(question_with_lang, model=model)

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


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="Multi LLM Chat In Console.(Using DashScope API)"
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
    parser.add_argument(
        "--continue",
        "-c",
        action="store_true",
        dest="continuous",
        help="Enable continuous conversation mode",
    )

    args = parser.parse_args()

    # 如果请求列出模型，则显示模型列表并退出
    if args.list_models:
        list_models()
        return

    # 初始化客户端和控制台
    client = DeepSeekClient()
    console = Console()

    # 判断是否启用连续对话
    if args.continuous or not args.question:
        # 命令行有 -c 参数，或者没有提供问题（交互式输入），都进入连续对话
        if args.question:
            # 如果有命令行问题，先处理第一个问题
            first_question = " ".join(args.question)
            single_chat(client, console, first_question, args.model)
            console.print("\n" + "=" * 50 + "\n")

        # 进入连续对话模式
        continuous_chat(client, console, args.model)
    else:
        # 单次对话模式
        question = " ".join(args.question)
        single_chat(client, console, question, args.model)


if __name__ == "__main__":
    main()
