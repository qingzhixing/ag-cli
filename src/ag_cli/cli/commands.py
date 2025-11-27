# cli/commands.py
from ag_cli.chat.interface import ChatInterface
from ag_cli.chat.history_manager import HistoryManager
from ag_cli.chat.input_handler import get_user_input


def continuous_chat(client, console, model=None, initial_question=None):
    """连续对话模式"""
    chat_interface = ChatInterface(client, console)
    history_manager = HistoryManager(chat_interface.system_prompt)

    console.print("[bold]输入 '.' 单独一行结束多行输入[/bold]")
    console.print("[bold]输入 '.exit' 结束对话[/bold]")
    console.print("[bold]输入 '.clear' 清空对话历史[/bold]")
    console.print("[bold]输入 '.history' 查看对话历史[/bold]\n")

    # 如果有初始问题，先处理
    if initial_question:
        # 显示问题
        chat_interface.display_question(initial_question)

        # 添加到对话历史
        history_manager.add_user_message(initial_question)

        try:
            # 调用API并动态显示结果
            response = chat_interface.call_api_continuous(
                history_manager.get_managed_history(), model
            )

            # 显示回答
            if response:
                # 将AI回复添加到对话历史
                history_manager.add_assistant_message(response)

        except Exception as e:
            console.print(f"[red]✖️ API调用错误: {str(e)}[/red]")
            # 移除最后一条用户消息，因为处理失败了
            if (
                history_manager.conversation_history
                and history_manager.conversation_history[-1]["role"] == "user"
            ):
                history_manager.conversation_history.pop()

    while True:
        try:
            # 获取用户输入
            user_input, should_exit = get_user_input(console, history_manager)

            if should_exit:
                return  # 退出对话

            if not user_input or not user_input.strip():
                continue  # 跳过空输入

            # 显示问题
            chat_interface.display_question(user_input)

            # 添加到对话历史
            history_manager.add_user_message(user_input)

            try:
                # 调用API并动态显示结果
                response = chat_interface.call_api_continuous(
                    history_manager.get_managed_history(), model
                )

                if response:
                    # 将AI回复添加到对话历史
                    history_manager.add_assistant_message(response)

            except Exception as e:
                console.print(f"[red]✖️ API调用错误: {str(e)}[/red]")
                # 移除最后一条用户消息，因为处理失败了
                if (
                    history_manager.conversation_history
                    and history_manager.conversation_history[-1]["role"] == "user"
                ):
                    history_manager.conversation_history.pop()

        except KeyboardInterrupt:
            console.print("\n[yellow]🛑 结束对话。[/yellow]")
            break


def single_chat(client, console, question, model=None):
    """单次对话模式"""
    chat_interface = ChatInterface(client, console)

    try:
        # 显示问题
        chat_interface.display_question(question)

        # 调用API并动态显示结果
        chat_interface.call_api_single(question, model)

    except Exception as e:
        console.print(f"[red]✖️ 错误: {str(e)}[/red]")


def config_command(args):
    """配置管理命令"""
    from ag_cli.config import (
        set_api_key,
        get_api_key,
        clear_api_key,
        get_config_file_path,
        get_config_dir_path,
        config_exists,
    )
    from rich.console import Console

    console = Console()

    if args.action == "set":
        if not args.api_key:
            console.print("[red]✖️ 请使用 --api-key 参数指定API密钥[/red]")
            return
        result = set_api_key(args.api_key)
        console.print(f"[green]✅ {result}[/green]")

        # 显示配置文件信息
        console.print(f"[cyan]📁 配置目录: {get_config_dir_path()}[/cyan]")
        console.print(f"[cyan]📄 配置文件: {get_config_file_path()}[/cyan]")

    elif args.action == "get":
        api_key = get_api_key()
        if api_key:
            # 显示部分密钥，保护敏感信息
            masked_key = api_key[:8] + "*" * (len(api_key) - 12) + api_key[-4:]
            console.print(f"[yellow]🔑 当前API密钥: {masked_key}[/yellow]")

            # 显示配置文件信息
            if config_exists():
                console.print(
                    f"[green]✅ 配置文件存在: {get_config_file_path()}[/green]"
                )
            else:
                console.print("[yellow]⚠️ 配置文件不存在，使用系统环境变量[/yellow]")

            console.print(f"[cyan]📁 配置目录: {get_config_dir_path()}[/cyan]")
        else:
            console.print("[red]✖️ 未设置API密钥[/red]")
            console.print(f"[cyan]📁 配置目录: {get_config_dir_path()}[/cyan]")
            console.print(f"[cyan]📄 配置文件: {get_config_file_path()}[/cyan]")

    elif args.action == "clear":
        result = clear_api_key()
        console.print(f"[green]✅ {result}[/green]")

        # 显示配置文件信息
        console.print(f"[cyan]📁 配置目录: {get_config_dir_path()}[/cyan]")
        console.print(f"[cyan]📄 配置文件: {get_config_file_path()}[/cyan]")
