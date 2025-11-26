from typing import Optional
from rich.console import Console
from rich.panel import Panel
from rich.live import Live
from rich import print as rprint
from rich.markdown import Markdown
from stream_processor import StreamProcessor


class RichOutputManager:
    """管理 Rich 输出和显示"""

    def __init__(self):
        self.console = Console()

    def display_question(self, question: str):
        """显示问题面板"""
        self.console.print(
            Panel.fit(
                f"[bold cyan]{question}[/bold cyan]",
                title="[bold blue]问题[/bold blue]",
                border_style="blue",
            )
        )
        self.console.print("\n[bold green]回答:[/bold green]\n")

    def display_thinking_spinner(self):
        """显示思考中的加载动画"""
        return self.console.status("[bold green]思考中...", spinner="dots")

    def display_stream_response(self, stream, question: str) -> str:
        """显示流式响应"""
        self.display_question(question)

        processor = StreamProcessor()
        code_blocks = []

        # 使用 Live 显示实时输出
        with Live(
            processor.regular_text, refresh_per_second=15, vertical_overflow="visible"
        ) as live:
            for chunk in stream:
                if (
                    hasattr(chunk.choices[0].delta, "content")
                    and chunk.choices[0].delta.content is not None
                ):
                    content = chunk.choices[0].delta.content

                    needs_update, code_block = processor.process_chunk(content)

                    if code_block:
                        code_blocks.append(code_block)
                        # 立即显示完成的代码块
                        self.console.print(code_block)
                        self.console.print()  # 代码块后添加空行

                    if needs_update:
                        live.update(processor.regular_text)

        # 处理最终可能未完成的代码块
        final_code_block = processor.get_final_code_block()
        if final_code_block:
            self.console.print(final_code_block)
            self.console.print()

        # 返回完整响应文本
        full_response = processor.get_final_regular_text().plain
        full_response += "".join(str(cb) for cb in code_blocks)
        if final_code_block:
            full_response += str(final_code_block)

        return full_response

    def display_error(self, error_message: str):
        """显示错误信息"""
        self.console.print(
            Panel.fit(
                f"[red]{error_message}[/red]",
                title="[bold red]错误[/bold red]",
                border_style="red",
            )
        )

    def display_raw_markdown(self, text: str):
        """将文本作为 Markdown 显示（备用方案）"""
        markdown = Markdown(text)
        self.console.print(markdown)
