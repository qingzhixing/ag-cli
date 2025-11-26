# main.py
import argparse
from .api_client import DeepSeekClient
from rich.console import Console
from .utils.models import list_models
from .cli.commands import continuous_chat, single_chat


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="Multi LLM Chat In Console.(Using DashScope API)"
    )
    parser.add_argument("question", nargs="*", help="Input question for AI")
    parser.add_argument(
        "--model", "-m", type=str, default=None, help="Model name or alias"
    )
    parser.add_argument(
        "--list-models",
        "-l",
        action="store_true",
        help="List all supported model aliases",
    )
    parser.add_argument(
        "--continue",
        "-c",
        action="store_true",
        dest="continuous",
        help="Enable continuous conversation mode",
    )

    args = parser.parse_args()

    # 如果请求列出模型，则显示模型列表并退出
    if args.list_models:
        list_models()
        return

    # 初始化客户端和控制台
    client = DeepSeekClient()
    console = Console()

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
