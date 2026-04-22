# utils/api.py

import os
import requests
import streamlit as st
from dotenv import load_dotenv

# 仅在本地开发时加载 .env 文件
if not os.getenv("STREAMLIT_CLOUD"):   # Streamlit Cloud 不会设置这个变量，这里只是一个简单判断
    load_dotenv()

# 优先从 st.secrets 读取，其次从环境变量读取
try:
    api_key = st.secrets.get("ZHIPU_API_KEY", os.getenv("ZHIPU_API_KEY"))
    base_url = st.secrets.get("ZHIPU_API_URL", os.getenv("ZHIPU_API_URL"))
    model = st.secrets.get("ZHIPU_MODEL", os.getenv("ZHIPU_MODEL", "glm-4-flash"))
except Exception:
    api_key = os.getenv("ZHIPU_API_KEY")
    base_url = os.getenv("ZHIPU_API_URL")
    model = os.getenv("ZHIPU_MODEL", "glm-4-flash")

if not api_key:
    raise ValueError("请在 Streamlit Cloud 的 Secrets 中设置 ZHIPU_API_KEY，或在本地 .env 文件中设置")
if not base_url:
    raise ValueError("请在 Streamlit Cloud 的 Secrets 中设置 ZHIPU_API_URL，或在本地 .env 文件中设置")

def translate_with_zhipu(prompt: str, model_override: str = None, temperature: float = 0.7, max_tokens: int = 2000) -> str:
    """调用智谱 AI API 进行翻译"""
    used_model = model_override or model
    url = base_url.rstrip("/") + "/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": used_model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": temperature,
        "max_tokens": max_tokens,
    }

    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        return data["choices"][0]["message"]["content"]
    except Exception as e:
        return f"❌ API 调用失败：{str(e)}"