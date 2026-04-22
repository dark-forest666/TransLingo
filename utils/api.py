# utils/api.py

import os
import json
import requests
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 从环境读取智谱 AI 的 API 配置
api_key = os.getenv("ZHIPU_API_KEY")
base_url = os.getenv("ZHIPU_API_URL")

if not api_key:
    raise ValueError("请在 .env 文件中设置 ZHIPU_API_KEY")
if not base_url:
    raise ValueError("请在 .env 文件中设置 ZHIPU_API_URL，例如 https://open.bigmodel.cn/api/paas/v4")

def translate_with_zhipu(prompt: str, model: str = None, temperature: float = 0.7, max_tokens: int = 2000) -> str:
    """调用智谱 AI API 进行翻译（使用 requests 直接调用）"""
    model = model or os.getenv("ZHIPU_MODEL", "glm-4-flash")

    url = base_url.rstrip("/") + "/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": temperature,
        "max_tokens": max_tokens,
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30.0)
        response.raise_for_status()
        data = response.json()

        # 解析 OpenAI 兼容格式的返回结果
        content = data.get("choices", [{}])[0].get("message", {}).get("content")
        if content is not None:
            return content

        return json.dumps(data, ensure_ascii=False)

    except requests.exceptions.RequestException as e:
        return f"❌ API 请求失败：{str(e)}"
    except Exception as e:
        return f"❌ 未知错误：{str(e)}"