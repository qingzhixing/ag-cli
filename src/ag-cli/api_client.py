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

    def resolve_model_name(self, model_alias):
        """将模型代称解析为实际模型名称"""
        model_mapping = self.config["model_mapping"]

        if model_alias in model_mapping:
            return model_mapping[model_alias]
        else:
            # 如果不是代称，直接使用传入的值
            return model_alias

    def chat(self, message, model=None):
        """非流式聊天接口"""
        try:
            # 解析模型名称
            actual_model = (
                self.resolve_model_name(model)
                if model
                else self.config["default_model"]
            )

            response = self.client.chat.completions.create(
                model=actual_model,
                messages=[{"role": "user", "content": message}],
                stream=False,
            )
            return response.choices[0].message.content
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 401:
                raise ValueError("DASHSCOPE_API_KEY is invalid")
            elif e.response.status_code == 429:
                raise ValueError("Rate limit exceeded")
            else:
                raise e
        except Exception as e:
            raise Exception(f"API request failed: {str(e)}")
