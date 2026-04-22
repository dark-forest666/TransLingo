# app.py

import streamlit as st
from utils.api import translate_with_zhipu
from utils.prompts import build_prompt_tech_to_business, build_prompt_business_to_tech
from utils.jargon import calculate_jargon_density
from utils.glossary import explain_technical_terms

# 页面配置
st.set_page_config(page_title="TransLingo", layout="wide", page_icon="🔄")

# 标题
st.markdown("<h1 style='text-align: center;'>🔄 TransLingo｜跨部门沟通翻译器</h1>", unsafe_allow_html=True)
st.markdown("""
<p style='text-align: center; color: gray;'>让技术与业务人员互相听懂对方的话 —— 消除黑话，高效协作</p>
""", unsafe_allow_html=True)

st.divider()

# 布局：中间列放主要控件
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    direction = st.selectbox("🔄 翻译方向", ["技术 → 业务", "业务 → 技术"], index=0)
    original_text = st.text_area(
        "📝 原文",
        height=200,
        placeholder="例如：数据库连接池在高并发下出现死锁，需要调整超时参数。"
    )
    tone = st.select_slider("🎭 语气", options=["正式", "温和", "幽默", "强硬"], value="正式")
    show_jargon = st.checkbox("🔍 显示黑话指数", value=False)

    translate_btn = st.button("🚀 开始翻译", type="primary", use_container_width=True)

# 侧边栏示例
with st.sidebar:
    with st.expander("📚 看看示例"):
        st.markdown("**示例1（技术 → 业务）**")
        st.markdown("> 原文：这个bug是偶发的，跟线程调度有关，我开了trace再观察一下。")
        st.markdown("> 翻译：程序每运行100次大约有1次出现卡顿，我们已经在记录日志，24小时内给结论。")
        st.markdown("---")
        st.markdown("**示例2（业务 → 技术）**")
        st.markdown("> 原文：这个按钮感觉不够有行动力。")
        st.markdown("> 翻译：- 按钮背景色改为#0078D4<br>- 悬停时增加阴影<br>- 文案从'提交'改为'立即获取报告'", unsafe_allow_html=True)
        st.markdown("---")
        st.markdown("**示例3（幽默语气）**")
        st.markdown("> 原文：服务器又崩了，咋回事啊？")
        st.markdown("> 翻译：服务器像熬夜的程序员一样打了个盹，我们给它冲杯咖啡（重启）就好啦～")

# 处理翻译（点击翻译按钮时）
if translate_btn:
    if not original_text.strip():
        st.warning("⚠️ 请输入待翻译的原文")
        st.stop()

    # 根据方向选择 prompt 构造函数
    if direction == "技术 → 业务":
        prompt = build_prompt_tech_to_business(original_text, tone)
    else:
        prompt = build_prompt_business_to_tech(original_text, tone)

    with st.spinner("🤖 AI 正在翻译中..."):
        result = translate_with_zhipu(prompt)

    # 保存到 session_state，供后续使用
    st.session_state.translation_result = result
    st.session_state.original_text = original_text
    st.session_state.direction = direction
    st.session_state.show_jargon = show_jargon

# 显示翻译结果（如果 session_state 中有结果）
if "translation_result" in st.session_state:
    result = st.session_state.translation_result
    original_text_saved = st.session_state.original_text
    direction_saved = st.session_state.direction
    show_jargon_saved = st.session_state.show_jargon

    st.subheader("✨ 翻译结果")
    st.markdown(result)

    # ---------- 专业名词解释功能 ----------
    if direction_saved == "技术 → 业务":
        # 使用一个独立的按钮，并设置 key，避免冲突
        if st.button("📖 解释技术名词", key="explain_btn"):
            with st.spinner("🔍 正在提取名词并解释..."):
                explanation = explain_technical_terms(original_text_saved)
            st.session_state.explanation = explanation
        # 显示已经生成的解释（如果存在）
        if "explanation" in st.session_state:
            st.subheader("📚 技术名词小课堂")
            st.markdown(st.session_state.explanation)
    else:
        st.info("💡 当前为业务→技术翻译，原文主要是业务需求，如需解释技术名词，请切换到技术→业务方向。")

    # 黑话指数
    if show_jargon_saved:
        orig_density = calculate_jargon_density(original_text_saved)
        result_density = calculate_jargon_density(result)
        st.subheader("📊 黑话指数对比")
        col_a, col_b = st.columns(2)
        with col_a:
            st.metric("原文黑话密度", f"{orig_density:.1%}")
        with col_b:
            st.metric("译文黑话密度", f"{result_density:.1%}")
        st.bar_chart({"原文黑话密度": orig_density, "译文黑话密度": result_density})

