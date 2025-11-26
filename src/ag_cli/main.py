# main.py
import argparse
from .api_client import DeepSeekClient
from rich.console import Console
from .utils.models import list_models
from .cli.commands import continuous_chat, single_chat


def config_handler(args):
    """处理配置选项"""
    from .cli.commands import config_command

    # 创建一个简单的命名空间对象来模拟原来的args
    class ConfigArgs:
        def __init__(self, action, api_key=None):
            self.action = action
            self.api_key = api_key

    config_args = ConfigArgs(args.config_action, args.api_key)
    config_command(config_args)


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="Multi LLM Chat In Console.(Using DashScope API)"
    )

    # 主要参数：问题
    parser.add_argument("question", nargs="*", help="Input question for AI")

    # 模型选项
    parser.add_argument(
        "--model", "-m", type=str, default=None, help="Model name or alias"
    )

    # 连续对话选项
    parser.add_argument(
        "--continue",
        "-c",
        action="store_true",
        dest="continuous",
        help="Enable continuous conversation mode",
    )

    # 配置管理选项
    config_group = parser.add_argument_group("配置管理")
    config_group.add_argument(
        "--config",
        choices=["set", "get", "clear"],
        dest="config_action",
        help="配置操作: set(设置), get(查看), clear(清除)",
    )
    config_group.add_argument(
        "--api-key", type=str, help="API密钥（仅--config set时使用）"
    )

    # 模型列表选项
    parser.add_argument(
        "--list-models",
        "-l",
        action="store_true",
        help="List all supported model aliases",
    )

    args = parser.parse_args()
    console = Console()

    # 处理配置命令（优先级最高）
    if args.config_action:
        config_handler(args)
        return

    # 如果请求列出模型，则显示模型列表并退出
    if args.list_models:
        list_models()
        return

    # 主聊天功能
    client = DeepSeekClient()

    # 判断是否启用连续对话
    if args.continuous or not args.question:
        # 连续对话模式
        initial_question = " ".join(args.question) if args.question else None
        continuous_chat(client, console, args.model, initial_question)
    else:
        # 单次对话模式
        question = " ".join(args.question)
        single_chat(client, console, question, args.model)


if __name__ == "__main__":
    main()
