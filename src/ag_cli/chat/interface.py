# chat/interface.py
from rich.panel import Panel
from rich.markdown import Markdown


class ChatInterface:
    """聊天界面管理类"""

    def __init__(self, client, console):
        self.client = client
        self.console = console
        self.system_prompt = "(如果我未指定语言，默认使用中文进行回答)"

    def display_question(self, question):
        """显示问题"""
        self.console.print(
            Panel.fit(
                f"[bold cyan]{question}[/bold cyan]",
                title="[bold blue]Question💭[/bold blue]",
                border_style="blue",
            )
        )

    def display_response(self, response):
        """显示AI回复"""
        self.console.print("\n[bold green]🤖:[/bold green]")

        if response is None:
            self.console.print("[yellow]✖️模型返回了空响应。[/yellow]")
        else:
            markdown = Markdown(response)
            self.console.print(markdown)

    def show_thinking(self):
        """显示思考状态"""
        return self.console.status("[bold green]🤔思考中...", spinner="dots")

    def call_api_single(self, question, model=None):
        """单次API调用"""
        question_with_lang = question + self.system_prompt

        with self.show_thinking():
            return self.client.chat(question_with_lang, model=model)

    def call_api_continuous(self, messages, model=None):
        """连续对话API调用"""
        with self.show_thinking():
            return self.client.chat_completion(messages, model=model)
