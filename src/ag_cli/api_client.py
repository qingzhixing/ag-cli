import httpx
from openai import OpenAI
from .config import load_config
from tenacity import retry, stop_after_attempt, wait_exponential
import time
from functools import wraps


def timing_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"⏱️ {func.__name__} took {end_time - start_time:.2f} seconds")
        return result

    return wrapper


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

    @retry(
        stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    @timing_decorator
    def chat(self, message, model=None):
        """流式聊天接口 - 单次对话"""
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
                stream=True,
            )

            # 收集流式响应
            full_response = ""
            for chunk in response:
                if chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    full_response += content

            return full_response

        except httpx.HTTPStatusError as e:
            if e.response.status_code == 401:
                raise ValueError("DASHSCOPE_API_KEY is invalid")
            elif e.response.status_code == 429:
                raise ValueError("Rate limit exceeded")
            else:
                raise e
        except Exception as e:
            raise Exception(f"API request failed: {str(e)}")

    @retry(
        stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    @timing_decorator
    def chat_completion(self, messages, model=None):
        """支持对话历史的流式聊天接口"""
        try:
            # 解析模型名称
            actual_model = (
                self.resolve_model_name(model)
                if model
                else self.config["default_model"]
            )

            response = self.client.chat.completions.create(
                model=actual_model,
                messages=messages,
                stream=True,
            )

            # 收集流式响应
            full_response = ""
            for chunk in response:
                if chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    full_response += content

            return full_response

        except httpx.HTTPStatusError as e:
            if e.response.status_code == 401:
                raise ValueError("DASHSCOPE_API_KEY is invalid")
            elif e.response.status_code == 429:
                raise ValueError("Rate limit exceeded")
            else:
                raise e
        except Exception as e:
            raise Exception(f"API request failed: {str(e)}")
