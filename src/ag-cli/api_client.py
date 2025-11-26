import httpx
from openai import OpenAI
from config import load_config


class DeepSeekClient:
    def __init__(self):
        self.config = load_config()
        self.client = OpenAI(
            api_key=self.config["api_key"],
            base_url=self.config["base_url"],
        )

    def stream_chat(self, message, model=None):
        """流式聊天接口"""
        try:
            stream = self.client.chat.completions.create(
                model=model or self.config["model"],
                messages=[{"role": "user", "content": message}],
                stream=True,
            )
            return stream
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 401:
                raise ValueError("DASHSCOPE_API_KEY is invalid")
            elif e.response.status_code == 429:
                raise ValueError("Rate limit exceeded")
            else:
                raise e
        except Exception as e:
            raise Exception(f"API request failed: {str(e)}")
