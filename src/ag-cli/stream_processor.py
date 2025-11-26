import re
from typing import Optional, Tuple
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
        self.pending_code_blocks = []
    
    def process_chunk(self, content: str) -> Tuple[bool, Optional[Syntax]]:
        """
        处理单个内容块
        返回: (是否需要更新显示, 可选的代码块)
        """
        self.buffer += content
        completed_code_block = None
        
        # 如果不在代码块中，检查是否有代码块开始
        if not self.in_code_block:
            # 查找代码块开始标记
            code_start_match = re.search(r'```(\w+)?\n?', self.buffer)
            if code_start_match:
                start_pos = code_start_match.start()
                end_pos = code_start_match.end()
                
                # 输出代码块前的文本
                if start_pos > 0:
                    text_before = self.buffer[:start_pos]
                    self.regular_text.append(text_before)
                
                # 开始代码块
                self.in_code_block = True
                self.current_language = code_start_match.group(1) or "text"
                
                # 剩余内容放入代码缓冲区
                self.code_buffer = self.buffer[end_pos:]
                self.buffer = ""
                
                return True, None
        
        # 处理代码块内的内容
        if self.in_code_block:
            # 检查代码块结束标记
            if '```' in self.code_buffer:
                code_parts = self.code_buffer.split('```', 1)
                code_content = code_parts[0]
                
                # 清理代码内容（移除多余的空格和空行）
                cleaned_code = self._clean_code_content(code_content)
                
                # 创建代码块语法高亮
                if cleaned_code.strip():  # 只有非空代码才创建语法高亮
                    completed_code_block = Syntax(
                        cleaned_code,
                        self.current_language,
                        theme="monokai",
                        line_numbers=True,
                        word_wrap=True
                    )
                
                # 重置代码块状态
                self.in_code_block = False
                self.current_language = ""
                
                # 处理代码块后的内容
                if len(code_parts) > 1 and code_parts[1]:
                    self.buffer = code_parts[1]
                else:
                    self.buffer = ""
                
                self.code_buffer = ""
                return True, completed_code_block
            
            # 代码块仍在继续，没有结束标记
            return False, None
        
        # 普通文本输出 - 直接添加到常规文本
        self.regular_text.append(content)
        self.buffer = ""  # 清空缓冲区，因为内容已经被处理
        return True, None
    
    def _clean_code_content(self, code_content: str) -> str:
        """清理代码内容，移除多余的空格和空行"""
        lines = code_content.split('\n')
        
        # 移除前后的空行
        while lines and not lines[0].strip():
            lines.pop(0)
        while lines and not lines[-1].strip():
            lines.pop()
        
        # 如果所有行都有相同的缩进，移除它
        if lines:
            # 计算最小缩进
            min_indent = float('inf')
            for line in lines:
                if line.strip():  # 只考虑非空行
                    indent = len(line) - len(line.lstrip())
                    min_indent = min(min_indent, indent)
            
            # 移除最小缩进
            if min_indent > 0 and min_indent != float('inf'):
                lines = [line[min_indent:] if len(line) > min_indent else line 
                        for line in lines]
        
        return '\n'.join(lines)
    
    def get_final_regular_text(self) -> Text:
        """获取最终的常规文本"""
        # 处理缓冲区中剩余的内容
        if self.buffer and not self.in_code_block:
            self.regular_text.append(self.buffer)
        
        # 如果仍在代码块中，将代码缓冲区的内容作为普通文本输出
        if self.in_code_block and self.code_buffer:
            self.regular_text.append(f"\n```{self.current_language}\n{self.code_buffer}")
        
        return self.regular_text
    
    def get_final_code_block(self) -> Optional[Syntax]:
        """获取最终未完成的代码块"""
        if self.in_code_block and self.code_buffer.strip():
            cleaned_code = self._clean_code_content(self.code_buffer)
            if cleaned_code.strip():
                return Syntax(
                    cleaned_code,
                    self.current_language or "text",
                    theme="monokai",
                    line_numbers=True,
                    word_wrap=True
                )
        return None