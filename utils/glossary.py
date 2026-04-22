# utils/glossary.py

import os
import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("ZHIPU_API_KEY")
base_url = os.getenv("ZHIPU_API_URL")

if not api_key or not base_url:
    raise ValueError("请先配置 ZHIPU_API_KEY 和 ZHIPU_API_URL")


def explain_technical_terms(original_text: str, model: str = None, temperature: float = 0.5) -> str:
    """
    从技术原文中提取专业名词，并给出通俗解释。
    返回格式为 Markdown 列表。
    """
    model = model or os.getenv("ZHIPU_MODEL", "glm-4-flash")
    url = base_url.rstrip("/") + "/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    prompt = f"""你是一个技术术语翻译官。请从下面的技术文本中，提取出最重要的专业名词（最多8个），并为每个名词提供一句通俗易懂的解释（面向业务人员，不要用复杂术语）。

要求：
- 只输出名词和解释，不要有其他废话。
- 格式为 Markdown 无序列表，每个名词加粗，例如：
  **死锁**：两个或多个任务互相等待对方释放资源，导致全部卡住。
  **连接池**：预先创建的一组数据库连接，可以重复使用，避免频繁创建销毁。

技术文本：
{original_text}

请输出："""

    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": temperature,
        "max_tokens": 800,
    }

    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        return data["choices"][0]["message"]["content"]
    except Exception as e:
        return f"❌ 解释失败：{str(e)}"