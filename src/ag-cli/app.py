from typing import Optional
from api_client import DeepSeekClient
from output_manager import RichOutputManager


class DeepSeekChatApp:
    """DeepSeek 聊天应用主类"""

    def __init__(self):
        self.client = DeepSeekClient()
        self.output_manager = RichOutputManager()

    def run(self, question: Optional[str] = None, model: Optional[str] = None):
        """运行聊天应用"""
        # 获取问题
        if not question:
            question = input("请输入您的问题: ")

        if not question.strip():
            self.output_manager.display_error("问题不能为空！")
            return

        try:
            # 显示加载动画并获取流式响应
            with self.output_manager.display_thinking_spinner():
                stream = self.client.stream_chat(question, model=model)

            # 处理并显示响应
            self.output_manager.display_stream_response(stream, question)

        except Exception as e:
            self.output_manager.display_error(str(e))
