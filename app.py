import streamlit as st
from openai import OpenAI
from datetime import datetime, timedelta
import json
import os
from dotenv import load_dotenv
import time

# 환경변수 로드
load_dotenv()

# 페이지 설정
st.set_page_config(
    page_title="AI 챗봇 상호작용 연구",
    page_icon="💬",
    layout="wide"
)

# OpenAI API 키 확인 및 클라이언트 초기화
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if OPENAI_API_KEY:
    client = OpenAI(api_key=OPENAI_API_KEY)
else:
    client = None

# 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []
if "session_start_time" not in st.session_state:
    st.session_state.session_start_time = None
if "session_active" not in st.session_state:
    st.session_state.session_active = False
if "participant_id" not in st.session_state:
    st.session_state.participant_id = None

# 세션 시간 제한 (20분 = 1200초)
SESSION_DURATION = 20 * 60  # 20분

def save_conversation(participant_id, messages):
    """대화 기록을 JSON 파일로 저장"""
    os.makedirs("conversations", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"conversations/{participant_id}_{timestamp}.json"
    
    conversation_data = {
        "participant_id": participant_id,
        "timestamp": timestamp,
        "session_start": st.session_state.session_start_time.isoformat() if st.session_state.session_start_time else None,
        "session_end": datetime.now().isoformat(),
        "messages": messages
    }
    
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(conversation_data, f, ensure_ascii=False, indent=2)
    
    return filename

def get_remaining_time():
    """남은 세션 시간 계산"""
    if not st.session_state.session_start_time:
        return SESSION_DURATION
    
    elapsed = (datetime.now() - st.session_state.session_start_time).total_seconds()
    remaining = max(0, SESSION_DURATION - elapsed)
    return remaining

def format_time(seconds):
    """초를 분:초 형식으로 변환"""
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{minutes:02d}:{secs:02d}"

def start_session(participant_id):
    """새 세션 시작"""
    st.session_state.participant_id = participant_id
    st.session_state.session_start_time = datetime.now()
    st.session_state.session_active = True
    st.session_state.messages = []
    st.rerun()

def end_session():
    """세션 종료 및 저장"""
    if st.session_state.participant_id and st.session_state.messages:
        filename = save_conversation(
            st.session_state.participant_id,
            st.session_state.messages
        )
        st.success(f"대화가 저장되었습니다: {filename}")
    
    st.session_state.session_active = False
    st.session_state.session_start_time = None
    st.session_state.messages = []
    st.session_state.participant_id = None

# 메인 UI
st.title("💬 AI 챗봇 상호작용 연구")

# API 키 확인 (최우선)
if not OPENAI_API_KEY:
    st.error("⚠️ **오류: OpenAI API 키가 설정되지 않았습니다.**")
    st.info("""
    연구 진행을 위해 관리자가 API 키를 설정해야 합니다.
    
    설정 방법:
    1. 프로젝트 폴더에 `.env` 파일을 생성하세요
    2. 다음 내용을 입력하세요: `OPENAI_API_KEY=your_api_key_here`
    3. 앱을 재시작하세요
    """)
    st.stop()

# 세션이 시작되지 않은 경우
if not st.session_state.session_active:
    st.markdown("### 연구 참여 안내")
    st.info("""
    본 연구는 AI 챗봇과의 대화를 통한 상호작용 연구입니다.
    - 대화 시간: 최대 20분
    - 참여자 ID를 입력하고 시작 버튼을 눌러주세요
    """)
    
    col1, col2 = st.columns([3, 1])
    with col1:
        participant_id = st.text_input(
            "참여자 ID",
            placeholder="예: P001, P002 등",
            key="participant_input",
            label_visibility="visible"
        )
    with col2:
        st.write("")  # 공간 맞추기
        st.write("")  # 공간 맞추기
        start_button = st.button("세션 시작", type="primary", use_container_width=True)
    
    if start_button:
        if participant_id and participant_id.strip():
            start_session(participant_id.strip())
        else:
            st.error("⚠️ 참여자 ID를 입력해주세요.")

else:
    # 세션 진행 중
    remaining_time = get_remaining_time()
    
    # 상단 정보 바
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.write(f"**참여자 ID:** {st.session_state.participant_id}")
    with col2:
        st.write(f"**남은 시간:** {format_time(remaining_time)}")
    with col3:
        if st.button("세션 종료", type="secondary"):
            end_session()
            st.rerun()
    
    # 시간 초과 확인
    if remaining_time <= 0:
        st.error("⏰ 세션 시간이 종료되었습니다.")
        end_session()
        st.rerun()
    
    # 채팅 인터페이스
    st.divider()
    
    # 대화 기록 표시
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
    
    # 사용자 입력
    if prompt := st.chat_input("메시지를 입력하세요..."):
        # 사용자 메시지 추가
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # AI 응답 생성
        with st.chat_message("assistant"):
            with st.spinner("응답 생성 중..."):
                try:
                    # OpenAI API 호출
                    response = client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "system", "content": "당신은 친근하고 도움이 되는 대화 상대입니다. 자연스럽고 진솔한 대화를 나누세요."},
                            *[{"role": msg["role"], "content": msg["content"]} 
                              for msg in st.session_state.messages]
                        ],
                        temperature=0.7,
                        max_tokens=500
                    )
                    
                    assistant_response = response.choices[0].message.content
                    st.markdown(assistant_response)
                    
                    # AI 메시지 추가
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": assistant_response
                    })
                    
                except Exception as e:
                    error_msg = f"오류가 발생했습니다: {str(e)}"
                    st.error(error_msg)
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": error_msg
                    })
        
        st.rerun()
    
    # 타이머 자동 업데이트 (Streamlit의 자동 새로고침 활용)
    if remaining_time > 0:
        # 남은 시간이 1분 이하일 때는 더 자주 업데이트
        refresh_interval = 1 if remaining_time <= 60 else 5
        time.sleep(refresh_interval)
        st.rerun()
