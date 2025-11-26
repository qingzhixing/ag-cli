# chat/history_manager.py
from rich.console import Console


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


class HistoryManager:
    """对话历史管理类"""

    def __init__(self, system_prompt):
        self.conversation_history = []
        self.system_prompt = system_prompt
        self.reset_history()

    def reset_history(self):
        """重置对话历史"""
        self.conversation_history = [{"role": "system", "content": self.system_prompt}]

    def add_user_message(self, message):
        """添加用户消息"""
        self.conversation_history.append({"role": "user", "content": message})

    def add_assistant_message(self, message):
        """添加AI回复"""
        self.conversation_history.append({"role": "assistant", "content": message})

    def get_managed_history(self):
        """获取管理后的对话历史（防止过长）"""
        return manage_context(self.conversation_history)

    def display_history(self, console):
        """显示对话历史"""
        console.print("\n[bold yellow]对话历史:[/bold yellow]")
        for i, msg in enumerate(self.conversation_history[1:], 1):  # 跳过系统消息
            role = "😎" if msg["role"] == "user" else "🤖"
            content_preview = (
                msg["content"][:100] + "..."
                if len(msg["content"]) > 100
                else msg["content"]
            )
            console.print(f"  {i}. {role}: {content_preview}")
        console.print()
