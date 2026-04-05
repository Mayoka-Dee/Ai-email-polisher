import streamlit as st
import requests

# 请替换成你新生成的智谱 API Key
API_KEY = "f1d79b8756794c268b81df272615b643.uYcRdEk7bN1D4kP6"

URL = "https://open.bigmodel.cn/api/paas/v4/chat/completions"

st.set_page_config(page_title="英文邮件润色器", page_icon="✉️")
st.title("✉️ 英文邮件润色器")
st.write("输入中文内容，选择语气，AI 会帮你写出英文邮件。")

# 语气选择
tone = st.selectbox("选择邮件语气：", ["正式", "友好"])

# 输入框
user_input = st.text_area("你的中文内容：", height=150)

# 按钮
if st.button("生成英文邮件"):
    if user_input.strip():
        # 根据语气构造系统提示
        if tone == "正式":
            system_prompt = "你是一个专业的英文邮件写作助手。请把用户输入的中文内容改写成正式、礼貌的英文邮件。只输出英文邮件正文，不要添加额外解释。"
        else:
            system_prompt = "你是一个友好的英文邮件写作助手。请把用户输入的中文内容改写成亲切、轻松的英文邮件。只输出英文邮件正文，不要添加额外解释。"

        with st.spinner("AI 正在生成邮件..."):
            headers = {
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": "glm-4-flash",
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_input}
                ]
            }
            try:
                response = requests.post(URL, json=payload, headers=headers, timeout=30)
                if response.status_code == 200:
                    result = response.json()
                    answer = result["choices"][0]["message"]["content"]
                    st.success("生成的英文邮件：")
                    st.write(answer)
                else:
                    st.error(f"API 调用失败：{response.text}")
            except Exception as e:
                st.error(f"请求出错：{e}")
    else:
        st.warning("请输入中文内容。")
