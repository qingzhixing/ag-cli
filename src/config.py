import os
from dotenv import load_dotenv


def validate_config(config):
    """验证配置"""
    required_keys = ["api_key", "base_url", "default_model", "model_mapping"]
    for key in required_keys:
        if key not in config:
            raise ValueError(f"Missing required config key: {key}")

    if not config["api_key"]:
        raise ValueError("API key cannot be empty")

    return config


def load_config():
    """加载配置文件和环境变量"""
    load_dotenv()

    dashscope_api_key = os.getenv("DASHSCOPE_API_KEY")
    if not dashscope_api_key:
        raise ValueError("DASHSCOPE_API_KEY not found in environment variables")

    # 模型名称映射
    model_mapping = {
        "v3.1": "deepseek-v3.1",
        "r1": "deepseek-r1",
        "q3m": "qwen3-max",
    }

    config = {
        "api_key": dashscope_api_key,
        "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
        "default_model": "deepseek-v3.1",
        "model_mapping": model_mapping,
    }

    return validate_config(config)
