import os
import httpx
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

dashscope_api_key = os.getenv("DASHSCOPE_API_KEY")
if not dashscope_api_key:
    raise ValueError("DASHSCOPE_API_KEY not found in environment variables")

client = OpenAI(
    api_key=dashscope_api_key,
    # 以下是北京地域base_url，如果使用新加坡地域的模型，需要将base_url替换为：https://dashscope-intl.aliyuncs.com/compatible-mode/v1
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)
try:
    completion = client.chat.completions.create(
        model="qwen-plus", messages=[{"role": "user", "content": "你是谁？"}]
    )
except httpx.HTTPStatusError as e:
    if e.response.status_code == 401:
        raise ValueError("DASHSCOPE_API_KEY is invalid")
    elif e.response.status_code == 429:
        raise ValueError("Rate limit exceeded") from e
    else:
        raise e
print(completion.choices[0].message.content)
