# utils/jargon.py

import re

# 预定义的技术/业务术语列表
JARGON_TERMS = [
    "接口", "延迟", "数据库", "死锁", "高并发", "连接池", "框架", "算法",
    "部署", "参数", "需求", "按钮", "点击", "交互", "颜色", "字体", "阴影",
    "响应式", "线程", "调度", "trace", "bug", "偶发", "缓存", "负载",
    "回滚", "迭代", "对齐", "颗粒度", "闭环", "赋能", "底层", "协议"
]


def calculate_jargon_density(text: str) -> float:
    """计算文本中专业术语的密度（术语出现次数 / 总词数）"""
    if not text:
        return 0.0

    # 分词：按空格、标点分割
    words = re.findall(r'\b\w+\b', text.lower())
    total_words = len(words)
    if total_words == 0:
        return 0.0

    # 统计术语出现次数（不区分大小写，子串匹配）
    term_count = 0
    text_lower = text.lower()
    for term in JARGON_TERMS:
        term_count += text_lower.count(term.lower())

    # 密度 = 术语出现总次数 / 总词数（可超过1，因为一个词可能含多个术语）
    density = term_count / total_words
    return min(density, 1.0)  # 限制最大为1