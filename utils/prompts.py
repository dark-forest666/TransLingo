# utils/prompts.py

def build_prompt_tech_to_business(original_text: str, tone: str) -> str:
    """将技术黑话翻译成业务人员能听懂的语言"""
    tone_instruction = {
        "正式": "使用专业但易懂的词汇，保持客观。",
        "温和": "语气柔和，避免让人感到被指责。",
        "幽默": "适当加入轻松、有趣的比喻。",
        "强硬": "直接指出问题，建议明确。"
    }.get(tone, "保持自然语气。")

    return f"""你是一个精通技术和业务的双语翻译官。请将下面这段「技术人员说的话」翻译成「非技术背景的业务人员/客户」能听懂的版本。

要求：
1. 保留所有关键事实，但去掉技术术语（如死锁、连接池、高并发、线程调度等）。
2. 用生活化的类比解释原理（例如“就像收银台排队，现在开了更多窗口”）。
3. 如果原文有抱怨或紧张情绪，转化为客观问题 + 下一步行动。
4. 最后加一行“💡 业务可以这样做：……”。
5. 语气：{tone_instruction}

原文：
{original_text}

请直接输出翻译结果，不要添加额外解释。"""


def build_prompt_business_to_tech(original_text: str, tone: str) -> str:
    """将业务人员的模糊需求翻译成技术可落地的描述"""
    tone_instruction = {
        "正式": "使用标准的技术术语，清晰准确。",
        "温和": "委婉地指出需求中的模糊点。",
        "幽默": "轻松提醒，避免让业务人员感到尴尬。",
        "强硬": "直接要求明确参数，不留模糊空间。"
    }.get(tone, "保持专业语气。")

    return f"""你是一个精通技术和业务的双语翻译官。请将下面这段「业务人员说的话」翻译成「技术人员能直接开发」的清晰需求描述。

要求：
1. 提取模糊需求中的具体参数（例如颜色、尺寸、速度、响应时间、交互方式等）。
2. 如果需求不明确，请用“[待确认]”标注并给出建议的默认值。
3. 输出格式：分条列出技术实现要点，每条用“- ”开头。
4. 语气：{tone_instruction}

原文：
{original_text}

请直接输出翻译结果，不要添加额外解释。""""""prompts.py
存放 prompt 构造函数的占位模块
"""


def build_translation_prompt(text: str, target_language: str = "zh") -> str:
    """构造一个简单的翻译 prompt（占位实现）。

    Args:
        text: 要翻译的文本
        target_language: 目标语言代码（默认中文 zh）

    Returns:
        str: 传递给模型的 prompt 文本
    """
    return f"Translate the following text to {target_language}: {text}"
