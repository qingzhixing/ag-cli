# cli/commands.py
from chat.interface import ChatInterface
from chat.history_manager import HistoryManager
from chat.input_handler import get_user_input


def continuous_chat(client, console, model=None):
    """连续对话模式"""
    chat_interface = ChatInterface(client, console)
    history_manager = HistoryManager(chat_interface.system_prompt)

    console.print("[bold]输入 '.' 单独一行结束多行输入[/bold]")
    console.print("[bold]输入 '.exit' 结束对话[/bold]")
    console.print("[bold]输入 '.clear' 清空对话历史[/bold]")
    console.print("[bold]输入 '.history' 查看对话历史[/bold]\n")

    while True:
        try:
            # 获取用户输入
            user_input, should_exit = get_user_input(console, history_manager)

            if should_exit:
                return  # 退出对话

            if not user_input or not user_input.strip():
                continue  # 跳过空输入

            # 添加到对话历史
            history_manager.add_user_message(user_input)

            try:
                # 获取管理后的历史并调用API
                managed_history = history_manager.get_managed_history()
                response = chat_interface.call_api_continuous(managed_history, model)

                # 显示回答
                chat_interface.display_response(response)

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

        # 调用API并显示结果
        response = chat_interface.call_api_single(question, model)
        chat_interface.display_response(response)

    except Exception as e:
        console.print(f"[red]✖️ 错误: {str(e)}[/red]")
