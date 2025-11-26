import os
from dotenv import load_dotenv


def load_config():
    """加载配置文件和环境变量"""
    load_dotenv()

    dashscope_api_key = os.getenv("DASHSCOPE_API_KEY")
    if not dashscope_api_key:
        raise ValueError("DASHSCOPE_API_KEY not found in environment variables")

    config = {
        "api_key": dashscope_api_key,
        "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
        "model": "deepseek-v3.1",
    }

    return config
