# 修改main.py，处理load_config抛出的异常
import argparse
from .api_client import DeepSeekClient
from rich.console import Console
from .utils.models import list_models
from .cli.commands import continuous_chat, single_chat
from .config import get_config_dir_path, get_config_file_path


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

    # 美化输出选项组
    pretty_group = parser.add_mutually_exclusive_group()
    pretty_group.add_argument(
        "--pretty",
        "-p",
        action="store_true",
        help="启用美化输出（响应时间、问题展示、Markdown渲染）",
    )
    pretty_group.add_argument(
        "--no-pretty",
        action="store_true",
        help="禁用美化输出（纯文本模式，适合重定向到文件）",
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

    # 确定美化模式
    if args.no_pretty:
        use_pretty = False
    elif args.pretty:
        use_pretty = True
    else:
        # 默认行为：连续对话启用美化，单次对话禁用美化
        use_pretty = args.continuous or not args.question

    # 主聊天功能
    try:
        # 创建API客户端时传递美化模式参数
        client = DeepSeekClient(use_pretty=use_pretty)
    except ValueError as e:
        # 处理缺少API密钥的情况
        console.print(f"[red]✖️ {str(e)}[/red]")
        console.print(f"[cyan]📁 配置目录: {get_config_dir_path()}[/cyan]")
        console.print(f"[cyan]📄 配置文件: {get_config_file_path()}[/cyan]")
        return

    # 判断是否启用连续对话
    if args.continuous or not args.question:
        # 连续对话模式
        initial_question = " ".join(args.question) if args.question else None
        continuous_chat(client, console, args.model, initial_question, use_pretty)
    else:
        # 单次对话模式
        question = " ".join(args.question)
        single_chat(client, console, question, args.model, use_pretty)


if __name__ == "__main__":
    main()
