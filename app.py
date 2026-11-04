
import os, base64, json, requests
import streamlit as st
from openai import OpenAI

# OpenAI 클라이언트 생성
client = OpenAI()

# 페이지 설정
st.set_page_config(page_title="음성 AI 서비스", page_icon="🤖", layout="wide")
st.title("음성 인식 AI 서비스")
st.write("음성으로 질문하시면 답변해 드립니다.")

# 역할 지정
sys_role = """
당신은 다양한 업무를 처리하는 AI 서비스입니다.
개인 비서처럼 친절하게 응대합니다.
"""

# 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

# 지시 영역
with st.form("task_form"):
    uploaded_file = st.file_uploader("텍스트 파일 업로드", type=["txt"])
    audio_value = st.audio_input("무엇을 도와드릴까요?")
    submit = st.form_submit_button("실행")

# 버튼을 눌렀을 때만 실행
if submit:
    # 업로드 된 파일이 있으면 디코딩
    text = ""
    if uploaded_file is not None:
        text = uploaded_file.read().decode("utf-8")

    # 녹음이 없으면 녹음 요청
    if audio_value is None:
        st.warning("음성을 녹음해주세요.")
        st.stop()

    # 시스템 메세지
    system_content = sys_role
    if text:
        system_content += f"\n\n다음 내용을 참고하세요:\n{text}"
    input_messages = [{"role": "system", "content": system_content}]

    # STT: 음성 → 텍스트
    transcript = client.audio.transcriptions.create(
        model="whisper-1",
        file=("audio.wav", audio_value, "audio/wav"))

    # 사용자 메시지
    input_messages.append({"role": "user", "content": transcript.text})

    # LLM 호출 및 응답 듣기
    with st.spinner("답변을 준비하고 있습니다..."):
        # LLM 호출
        response = client.responses.create(
            model="gpt-4o-mini",
            input=input_messages
        )
        answer = response.output_text

        # 응답 출력
        st.subheader("AI 답변")
        st.write(answer)


import streamlit as st
from openai import OpenAI

# OpenAI 클라이언트
# 기존 app.py에 client가 이미 있다면 중복 선언하지 않아도 됩니다.
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
