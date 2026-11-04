
import os, base64, json, requests
import streamlit as st
from openai import OpenAI

# OpenAI 클라이언트
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# AI 번역 비서 역할 설정
sys_role = """
당신은 AI 번역 비서 '에이블'입니다.
사용자가 입력한 문장을 원하는 언어로 번역합니다.

규칙:
1. 원문의 의미를 정확하게 유지합니다.
2. 자연스럽고 유창한 표현을 사용합니다.
3. 사용자가 선택한 번역 스타일을 반영합니다.
4. 번역된 문장만 출력합니다.
5. 불필요한 설명은 하지 않습니다.
"""

st.title("🌍 AI 번역 비서 에이블")
st.write("원하는 언어와 스타일을 선택하여 번역해 보세요!")

# 번역할 문장 입력
text = st.text_area(
    "번역할 문장을 입력하세요",
    placeholder="번역할 문장을 입력해 주세요."
)

# 번역 언어 선택
language = st.selectbox(
    "번역할 언어를 선택하세요",
    ["영어", "일본어", "중국어(간체)", "스페인어", "프랑스어"]
)

# 번역 스타일 선택
style = st.selectbox(
    "번역 스타일을 선택하세요",
    [
        "자연스러운 일상 표현",
        "정중한 비즈니스 표현",
        "친근하고 편안한 표현"
    ]
)

# 번역 실행
if st.button("🌐 번역하기"):

    if not text.strip():
        st.warning("번역할 문장을 입력해 주세요.")

    else:
        prompt = f"""
        다음 문장을 번역해 주세요.

        [원문]
        {text}

        [번역 언어]
        {language}

        [번역 스타일]
        {style}
        """

        try:
            with st.spinner("에이블이 번역 중입니다..."):
                response = client.responses.create(
                    model="gpt-4o-mini",
                    input=[
                        {"role": "system", "content": sys_role},
                        {"role": "user", "content": prompt}
                    ]
                )

            st.success("번역 완료!")

            st.write("**원문:**", text)
            st.write("**번역 언어:**", language)
            st.write("**번역 스타일:**", style)

            st.subheader("번역 결과")
            st.write(response.output_text)

        except Exception as e:
            st.error(f"번역 중 오류가 발생했습니다: {e}")
