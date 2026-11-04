from io import BytesIO
import os, base64, json, requests
import streamlit as st
from openai import OpenAI

# OpenAI 클라이언트
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])


st.set_page_config(page_title="에이블 AI 번역 비서", page_icon="🌍", layout="centered")
st.title("🌍 AI 번역 비서 에이블")
st.caption("번역하고, 원하는 언어로 음성을 들어보세요.")

SYSTEM_ROLE = """당신은 AI 번역 비서 '에이블'입니다.
사용자가 입력한 문장을 지정된 언어로 번역합니다.
원문의 의미를 정확하게 유지하고 자연스럽고 유창하게 표현합니다.
선택한 번역 스타일을 반영합니다.
번역된 문장만 출력하고 설명은 추가하지 않습니다."""

LANGUAGES = ["영어", "일본어", "중국어(간체)", "스페인어", "프랑스어"]
STYLES = ["자연스러운 일상 표현", "정중한 비즈니스 표현", "친근하고 편안한 표현"]

if "translation_result" not in st.session_state:
    st.session_state.translation_result = None
if "translation_audio" not in st.session_state:
    st.session_state.translation_audio = None

with st.form("translation_form"):
    text = st.text_area("번역할 문장을 입력하세요", placeholder="예: 안녕하세요. 만나서 반갑습니다.", height=130)
    language = st.selectbox("번역 언어", LANGUAGES)
    style = st.selectbox("번역 스타일", STYLES)
    translate_clicked = st.form_submit_button("🌐 번역하기", use_container_width=True)

if translate_clicked:
    st.session_state.translation_result = None
    st.session_state.translation_audio = None
    if not text.strip():
        st.warning("번역할 문장을 입력해 주세요.")
    elif not st.secrets.get("OPENAI_API_KEY"):
        st.error("Streamlit Secrets에 OPENAI_API_KEY를 등록해 주세요.")
    else:
        try:
            client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
            with st.spinner("에이블이 번역 중입니다..."):
                response = client.responses.create(
                    model="gpt-4o-mini",
                    input=[
                        {"role": "system", "content": SYSTEM_ROLE},
                        {"role": "user", "content": f"다음 문장을 {language}로 번역해 주세요. 스타일: {style}\n\n원문:\n{text}"},
                    ],
                )
            translated_text = response.output_text.strip()
            if not translated_text:
                st.error("번역 결과가 비어 있습니다. 다시 시도해 주세요.")
            else:
                st.session_state.translation_result = {
                    "original": text,
                    "language": language,
                    "style": style,
                    "translated": translated_text,
                }
        except Exception as e:
            st.error(f"번역 중 오류가 발생했습니다: {e}")

result = st.session_state.translation_result
if result is not None:
    st.divider()
    st.subheader("🌍 번역 결과")
    st.write(result["translated"])
    st.caption(f"번역 언어: {result['language']} | 스타일: {result['style']}")
    st.subheader("🔊 번역 음성 듣기")
    st.info("아래 버튼을 누르면 AI 음성을 생성합니다. 음성 생성에는 별도 API 비용이 발생합니다.")
    if st.button("🎙️ 음성 생성하기", use_container_width=True):
        if not st.secrets.get("OPENAI_API_KEY"):
            st.error("Streamlit Secrets에 OPENAI_API_KEY를 등록해 주세요.")
        else:
            try:
                client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
                with st.spinner("음성을 생성 중입니다..."):
                    speech = client.audio.speech.create(
                        model="tts-1",
                        voice="alloy",
                        input=result["translated"],
                        response_format="mp3",
                    )
                st.session_state.translation_audio = speech.content
            except Exception as e:
                st.error(f"음성 생성 중 오류가 발생했습니다: {e}")
    if st.session_state.translation_audio is not None:
        st.audio(st.session_state.translation_audio, format="audio/mp3")
        st.download_button(
            "📥 MP3 다운로드",
            data=st.session_state.translation_audio,
            file_name="able_translation.mp3",
            mime="audio/mpeg",
        )
