# main.py
import argparse
from .api_client import DeepSeekClient
from rich.console import Console
from .utils.models import list_models
from .cli.commands import continuous_chat, single_chat, config_command


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="Multi LLM Chat In Console.(Using DashScope API)"
    )

    # 添加子命令
    subparsers = parser.add_subparsers(dest="command", help="可用命令")

    # 配置命令
    config_parser = subparsers.add_parser("config", help="管理配置")
    config_parser.add_argument(
        "action",
        choices=["set", "get", "clear"],
        help="配置操作: set(设置), get(查看), clear(清除)",
    )
    config_parser.add_argument("--api-key", type=str, help="API密钥（仅set操作需要）")

    # 模型列表命令
    list_parser = subparsers.add_parser("list-models", help="列出支持的模型")

    # 保持向后兼容：直接输入问题作为主命令
    parser.add_argument("question", nargs="*", help="Input question for AI")
    parser.add_argument(
        "--model", "-m", type=str, default=None, help="Model name or alias"
    )
    parser.add_argument(
        "--continue",
        "-c",
        action="store_true",
        dest="continuous",
        help="Enable continuous conversation mode",
    )
    parser.add_argument(
        "--list-models",
        "-l",
        action="store_true",
        help="List all supported model aliases",
    )

    args = parser.parse_args()

    console = Console()

    # 如果请求列出模型，则显示模型列表并退出
    if args.list_models:
        list_models()
        return

    # 处理配置命令
    if args.command == "config":
        config_command(args)
        return

    # 处理模型列表命令
    if args.command == "list-models":
        list_models()
        return

    # 主聊天功能（保持原有简洁格式）
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
