import re
from typing import Optional
from rich.syntax import Syntax
from rich.text import Text


class StreamProcessor:
    """处理流式响应，管理状态和缓冲区"""

    def __init__(self):
        self.buffer = ""
        self.current_language = ""
        self.in_code_block = False
        self.code_buffer = ""
        self.regular_text = Text()

    def process_chunk(self, content: str) -> tuple[bool, Optional[Syntax]]:
        """
        处理单个内容块
        返回: (是否需要更新显示, 可选的代码块)
        """
        self.buffer += content
        completed_code_block = None

        # 检查代码块开始
        if not self.in_code_block and "```" in self.buffer:
            parts = self.buffer.split("```", 1)
            if len(parts) > 1:
                # 输出代码块前的文本
                if parts[0]:
                    self.regular_text.append(parts[0])

                # 开始代码块
                self.in_code_block = True
                remaining = parts[1]

                # 检查是否有语言指定
                lang_match = re.match(r"^(\w+)\s*\n?", remaining)
                if lang_match:
                    self.current_language = lang_match.group(1)
                    remaining = remaining[lang_match.end() :]
                else:
                    self.current_language = ""

                self.code_buffer = remaining
                self.buffer = ""
                return True, None

        # 处理代码块内的内容
        elif self.in_code_block:
            self.code_buffer += content

            # 检查代码块结束
            if "```" in self.code_buffer:
                code_parts = self.code_buffer.split("```", 1)
                code_content = code_parts[0]

                # 创建代码块语法高亮
                completed_code_block = Syntax(
                    code_content.rstrip(),
                    self.current_language or "text",
                    theme="monokai",
                    line_numbers=True,
                    word_wrap=True,
                )

                # 重置代码块状态
                self.in_code_block = False
                self.current_language = ""
                self.code_buffer = ""

                # 处理代码块后的内容
                if len(code_parts) > 1 and code_parts[1]:
                    self.buffer = code_parts[1]

                return True, completed_code_block

            # 代码块仍在继续
            return False, None

        # 普通文本输出
        elif not self.in_code_block:
            self.regular_text.append(content)
            return True, None

        return False, None

    def get_final_regular_text(self) -> Text:
        """获取最终的常规文本"""
        if self.buffer and not self.in_code_block:
            self.regular_text.append(self.buffer)
        return self.regular_text

    def get_final_code_block(self) -> Optional[Syntax]:
        """获取最终未完成的代码块"""
        if self.in_code_block and self.code_buffer:
            return Syntax(
                self.code_buffer.rstrip(),
                self.current_language or "text",
                theme="monokai",
                line_numbers=True,
                word_wrap=True,
            )
        return None
