import argparse
from app import DeepSeekChatApp


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="DeepSeek AI Chat with Rich Output")
    parser.add_argument("question", nargs="*", help="Input question for AI")
    parser.add_argument("--model", "-m", type=str, default=None, help="Model name")

    args = parser.parse_args()

    # 获取问题
    question = " ".join(args.question) if args.question else None

    # 创建并运行应用
    app = DeepSeekChatApp()
    app.run(question=question, model=args.model)


if __name__ == "__main__":
    main()
