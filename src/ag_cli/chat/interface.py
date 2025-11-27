# chat/interface.py
from rich.panel import Panel
from rich.markdown import Markdown
from rich.live import Live
import re


class ChatInterface:
    """聊天界面管理类"""

    def __init__(self, client, console):
        self.client = client
        self.console = console
        self.system_prompt = "(如果未指定语言，回复答案时请使用中文语言)"

    def display_question(self, question):
        """显示问题"""
        self.console.print(
            Panel.fit(
                f"[bold cyan]{question}[/bold cyan]",
                title="[bold blue]Question💭[/bold blue]",
                border_style="blue",
            )
        )

    def display_streaming_response(self, response_stream):
        """动态显示流式AI回复"""
        self.console.print("\n[bold green]🤖:[/bold green]")

        full_response = ""
        with Live(refresh_per_second=10) as live:
            for chunk in response_stream:
                if chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    full_response += content

                    # 动态更新Markdown显示
                    processed_response = self._preprocess_response(full_response)
                    markdown = Markdown(processed_response)
                    live.update(markdown)

        return full_response

    def display_response(self, response):
        """显示AI回复"""
        self.console.print("\n[bold green]🤖:[/bold green]")

        if response is None:
            self.console.print("[yellow]✖️模型返回了空响应。[/yellow]")
        else:
            # 预处理响应，确保代码块正确渲染
            processed_response = self._preprocess_response(response)
            markdown = Markdown(processed_response)
            self.console.print(markdown)

    def _preprocess_response(self, response):
        """预处理响应，确保代码块正确渲染"""
        # 确保代码块有正确的语言标识
        response = re.sub(r"```(\w*)", r"```\1\n", response)
        response = re.sub(r"```\n", r"\n```\n", response)
        return response

    def call_api_single(self, question, model=None):
        """单次API调用 - 动态流式输出"""
        question_with_lang = question + self.system_prompt

        # 获取流式响应（不显示思考中）
        actual_model = (
            self.client.resolve_model_name(model)
            if model
            else self.client.config["default_model"]
        )

        response = self.client.client.chat.completions.create(
            model=actual_model,
            messages=[{"role": "user", "content": question_with_lang}],
            stream=True,
        )

        # 动态显示流式响应
        return self.display_streaming_response(response)

    def call_api_continuous(self, messages, model=None):
        """连续对话API调用 - 动态流式输出"""
        # 获取流式响应（不显示思考中）
        actual_model = (
            self.client.resolve_model_name(model)
            if model
            else self.client.config["default_model"]
        )

        response = self.client.client.chat.completions.create(
            model=actual_model,
            messages=messages,
            stream=True,
        )

        # 动态显示流式响应
        return self.display_streaming_response(response)
