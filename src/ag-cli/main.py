import argparse
from api_client import DeepSeekClient


def process_stream_response(stream):
    """处理流式响应，直接输出内容"""
    full_response = ""

    for chunk in stream:
        if (
            hasattr(chunk.choices[0].delta, "content")
            and chunk.choices[0].delta.content is not None
        ):
            content = chunk.choices[0].delta.content
            print(content, end="", flush=True)  # 直接输出，无延迟
            full_response += content

    print()  # 最后换行
    return full_response


def main():
    parser = argparse.ArgumentParser(
        description="DeepSeek AI Chat with Streaming Output"
    )
    parser.add_argument("--question", "-q", type=str, help="Input question for AI")
    parser.add_argument(
        "--model",
        "-m",
        type=str,
        default=None,
        help="Model name (default: deepseek-v3.1)",
    )

    args = parser.parse_args()

    # 获取问题
    if args.question:
        question = args.question
    else:
        question = input("请输入您的问题: ")

    if not question.strip():
        print("问题不能为空！")
        return

    # 初始化客户端
    client = DeepSeekClient()

    try:
        print(f"问题: {question}")
        print("回答: ", end="", flush=True)

        # 获取流式响应
        stream = client.stream_chat(question, model=args.model)

        # 处理并显示响应
        full_response = process_stream_response(stream)

    except Exception as e:
        print(f"\n错误: {str(e)}")


if __name__ == "__main__":
    main()
