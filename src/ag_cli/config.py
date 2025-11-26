import os
import json
from pathlib import Path
from rich.console import Console

console = Console()

# 配置文件路径
CONFIG_DIR = Path.home() / ".ag-cli"
CONFIG_FILE = CONFIG_DIR / "config.json"


def ensure_config_dir():
    """确保配置目录存在"""
    CONFIG_DIR.mkdir(exist_ok=True)


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
    # 优先级：1. 系统环境变量 2. 配置文件

    # 1. 检查系统环境变量
    dashscope_api_key = os.getenv("DASHSCOPE_API_KEY")

    # 2. 检查配置文件
    if not dashscope_api_key and CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                config_data = json.load(f)
                dashscope_api_key = config_data.get("api_key", "")
        except Exception as e:
            console.print(f"[yellow]⚠️ 读取配置文件失败: {str(e)}[/yellow]")

    if not dashscope_api_key:
        console.print(
            "[red]✖️ 未找到API密钥，请使用 'ag config set --api-key <your-key>' 设置[/red]"
        )
        console.print(f"[cyan]📁 配置目录: {get_config_dir_path()}[/cyan]")
        console.print(f"[cyan]📄 配置文件: {get_config_file_path()}[/cyan]")
        exit(1)

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


def set_api_key(api_key: str):
    """设置API密钥到配置文件"""
    ensure_config_dir()

    config_data = {
        "api_key": api_key,
        "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
        "default_model": "deepseek-v3.1",
    }

    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(config_data, f, indent=2, ensure_ascii=False)
        return f"API密钥已保存到配置文件: {CONFIG_FILE}"
    except Exception as e:
        return f"保存配置失败: {str(e)}"


def get_api_key() -> str:
    """获取当前API密钥"""
    # 优先级：1. 系统环境变量 2. 配置文件
    api_key = os.getenv("DASHSCOPE_API_KEY", "")

    if not api_key and CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                config_data = json.load(f)
                api_key = config_data.get("api_key", "")
        except Exception as e:
            console.print(f"[yellow]⚠️ 读取配置文件失败: {str(e)}[/yellow]")

    return api_key


def clear_api_key():
    """清除API密钥"""
    # 清除系统环境变量
    if "DASHSCOPE_API_KEY" in os.environ:
        del os.environ["DASHSCOPE_API_KEY"]

    # 删除配置文件
    if CONFIG_FILE.exists():
        try:
            CONFIG_FILE.unlink()
            return f"API密钥已清除，配置文件已删除: {CONFIG_FILE}"
        except Exception as e:
            return f"清除配置失败: {str(e)}"

    return "API密钥已清除"


def get_config_file_path():
    """获取配置文件路径"""
    return str(CONFIG_FILE)


def get_config_dir_path():
    """获取配置目录路径"""
    return str(CONFIG_DIR)


def config_exists():
    """检查配置文件是否存在"""
    return CONFIG_FILE.exists()
