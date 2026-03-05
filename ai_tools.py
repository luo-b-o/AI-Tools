#=====================================================
# AI 全能效率助手
# ✅ AI 文档总结（自动读 PDF，输出精简总结）
# ✅ AI 智能写作（文案、邮件、报告、自我介绍一键生成）
# ✅ AI 面试模拟（根据你的简历自动提问 + 给标准答案）
#=====================================================

#导入必要的库
import streamlit as st
from openai import OpenAI
import PyPDF2

#===================配置===================
API_KEY ="sk-ca465c9115bf4e659b6d179e2c4e6670"
client = OpenAI(
    api_key=API_KEY,
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

#===================界面===================
st.title("🤖 全能效率助手")
st.write("文档总结 | 智能写作 | 面试模拟")

#选项卡（Streamlit功能）
tab1,tab2,tab3 = st.tabs([
    "📄 PDF总结",
    "✍️ AI写作",
    "🎤 面试模拟"
])

#===================功能1：PDF总结===================
with tab1:
    st.subheader("📄 自动总结PDF内容")
    file = st.file_uploader("上传PDF",type="pdf",key="sum")
    if file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            t = page.extract_text()   
            if t:
                text += t
        st.success("✅ 读取成功")
        if st.button("开始总结"):
            with st.spinner("总结中。。。"):
                prompt = f"请总结这份内容，简洁清晰，分点输出: \n{text}"
                res = client.chat.completions.create(
                    model="qwen-turbo",
                    messages=[{"role":"user","content":prompt}]
                )
                st.write("### 📌 总结结果：")
                st.write(res.choices[0].message.content)

#===================功能2：AI写作====================
with tab2:
    st.subheader("✍️ AI智能写作工具")
    topic = st.text_input("输入写作主题：")
    style = st.selectbox("写作风格",["正式","简洁","活泼","专业"])
    if topic and st.button("开始写作"):
        with st.spinner("写作中。。。"):
            prompt = f"请以{style}风格写：{topic},结构清晰，内容实用"
            res = client.chat.completions.create(
                model="qwen-turbo",
                messages=[{"role":"user","content":prompt}]
            )
            st.write("### 📌 写作结果：")
            st.write(res.choices[0].message.content)

#===================功能3：面试模拟助手===============
with tab3:
    st.subheader("🎤 AI面试模拟助手")
    info = st.text_area("粘贴你的个人简历/个人介绍：")
    job = st.text_input("应聘岗位：")
    if info and job and st.button("生成面试题"):
        with st.spinner("生成中。。。"):
            prompt = f"""
根据一下简历和应聘岗位,生成10道高配面试题 + 简短的参考答案。
简历：{info}
岗位：{job}
"""

            res = client.chat.completions.create(
                model="qwen-turbo",
                messages=[{"role":"user","content":prompt}]
            )
            st.write("### 📌 面试题目：")
            st.write(res.choices[0].message.content)

