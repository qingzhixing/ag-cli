# chat/input_handler.py
def get_user_input(console, history_manager, use_pretty=True):
    """获取用户输入，处理特殊命令"""
    console.print(
        "\n[dim ][blue ]Tips[/blue ]: '.' in a line to end multi-line input.[/dim ]"
    )
    console.print("[bold cyan]😎:[/bold cyan] ", end="")

    lines = []

    while True:
        try:
            line = input()
            command = line.strip()

            # 处理特殊命令
            if command == ".exit":
                console.print("\n[yellow]🛑 结束对话。[/yellow]\n")
                return None, True

            elif command == ".clear":
                history_manager.reset_history()
                console.print("\n[green]✅ 对话历史已清空。[/green]\n")
                return None, False

            elif command == ".history":
                history_manager.display_history(console, use_pretty)
                if use_pretty:
                    console.print("\n")
                return None, False

            elif command == ".":
                break

            lines.append(line)

        except EOFError:
            break

    user_input = "\n".join(lines)
    return user_input, False
