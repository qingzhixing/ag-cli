# chat/interface.py
from rich.panel import Panel
from rich.markdown import Markdown
from rich.live import Live
import re
import time


class ChatInterface:
    """聊天界面管理类"""

    def __init__(self, client, console, use_pretty=True):
        self.client = client
        self.console = console
        self.use_pretty = use_pretty
        self.system_prompt = "(如果未指定语言，回复答案时请使用中文语言)"

    def display_question(self, question):
        """显示问题"""
        if self.use_pretty:
            self.console.print(
                Panel.fit(
                    f"[bold cyan]{question}[/bold cyan]",
                    title="[bold blue]Question💭[/bold blue]",
                    border_style="blue",
                )
            )
        else:
            # 纯文本模式
            self.console.print(f"问题: {question}")

    def display_streaming_response(self, response_stream):
        """动态显示流式AI回复"""
        if not self.use_pretty:
            # 纯文本模式 - 直接输出
            return self._display_plain_text_response(response_stream)

        # 美化模式 - 使用Markdown实时渲染
        self.console.print("\n[bold green]🤖:[/bold green]")

        full_response = ""
        last_update_time = time.time()
        update_interval = 0.3
        chunk_buffer = ""

        with Live(refresh_per_second=5, auto_refresh=False) as live:
            try:
                for chunk in response_stream:
                    if chunk.choices and chunk.choices[0].delta.content:
                        content = chunk.choices[0].delta.content
                        full_response += content
                        chunk_buffer += content

                        current_time = time.time()
                        if (
                            current_time - last_update_time >= update_interval
                            or len(chunk_buffer) >= 100
                        ):
                            processed_response = self._preprocess_response(
                                full_response
                            )
                            markdown = Markdown(processed_response)
                            live.update(markdown, refresh=True)
                            last_update_time = current_time
                            chunk_buffer = ""

                processed_response = self._preprocess_response(full_response)
                markdown = Markdown(processed_response)
                live.update(markdown, refresh=True)

            except Exception as e:
                self.console.print(f"[yellow]⚠️ 流式响应中断: {str(e)}[/yellow]")
                if full_response:
                    processed_response = self._preprocess_response(full_response)
                    markdown = Markdown(processed_response)
                    live.update(markdown, refresh=True)

        return full_response

    def _display_plain_text_response(self, response_stream):
        """纯文本模式显示响应"""
        full_response = ""
        for chunk in response_stream:
            if chunk.choices and chunk.choices[0].delta.content:
                content = chunk.choices[0].delta.content
                full_response += content
                # 实时输出到控制台
                print(content, end="", flush=True)

        print()  # 换行
        return full_response

    def display_response(self, response):
        """显示AI回复"""
        if not self.use_pretty:
            # 纯文本模式
            print(f"\n回答: {response}")
            return

        self.console.print("\n[bold green]🤖:[/bold green]")
        if response is None:
            self.console.print("[yellow]✖️模型返回了空响应。[/yellow]")
        else:
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
        """单次API调用"""
        question_with_lang = question + self.system_prompt
        response_stream = self.client.get_chat_stream(question_with_lang, model)
        return self.display_streaming_response(response_stream)

    def call_api_continuous(self, messages, model=None):
        """连续对话API调用"""
        response_stream = self.client.get_chat_completion_stream(messages, model)
        return self.display_streaming_response(response_stream)
