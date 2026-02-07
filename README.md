# AI 챗봇 상호작용 연구 플랫폼

IRB 승인 연구를 위한 Streamlit 기반 AI 챗봇 상호작용 플랫폼입니다.

## 기능

- 🤖 OpenAI GPT-3.5-turbo 기반 챗봇
- ⏱️ 20분 세션 타이머
- 💾 대화 기록 자동 저장 (JSON 형식)
- 👤 참여자 ID 관리

## 설치 방법

1. **저장소 클론 또는 파일 다운로드**

2. **가상환경 생성 및 활성화** (선택사항)
```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
# 또는
venv\Scripts\activate  # Windows
```

3. **필요한 패키지 설치**
```bash
pip install -r requirements.txt
```

4. **환경변수 설정**
```bash
cp .env.example .env
```
그리고 `.env` 파일을 열어서 OpenAI API 키를 입력하세요:
```
OPENAI_API_KEY=sk-your-actual-api-key-here
```

## 실행 방법

```bash
streamlit run app.py
```

브라우저에서 자동으로 열리며, 기본 주소는 `http://localhost:8501`입니다.

## 사용 방법

### 관리자 설정 (연구 진행 전)

1. **API 키 설정**
   - 프로젝트 루트에 `.env` 파일 생성
   - `OPENAI_API_KEY=your_api_key_here` 입력
   - API 키는 [OpenAI Platform](https://platform.openai.com/api-keys)에서 발급

2. **서버 실행**
   ```bash
   streamlit run app.py
   ```

3. **공개 URL 생성** (비대면 실험용)
   - Streamlit Cloud에 배포하거나
   - 로컬 서버를 ngrok 등으로 터널링하여 공개 URL 생성

### 참가자 사용 방법

1. **세션 시작**
   - 제공받은 링크로 접속
   - 참여자 ID 입력 (예: P001, P002 등)
   - "세션 시작" 버튼 클릭

2. **대화 진행**
   - 20분 동안 AI 챗봇과 자유롭게 대화
   - 상단에 남은 시간 실시간 표시
   - 자연스러운 대화 진행

3. **세션 종료**
   - 20분 경과 시 자동 종료 및 저장
   - 또는 "세션 종료" 버튼으로 수동 종료 가능

4. **데이터 저장**
   - 대화 기록은 `conversations/` 폴더에 자동 저장
   - 파일명 형식: `{참여자ID}_{타임스탬프}.json`
   - 연구자가 나중에 분석 가능

## 데이터 형식

저장되는 JSON 파일 구조:
```json
{
  "participant_id": "P001",
  "timestamp": "20260115_143022",
  "session_start": "2026-01-15T14:30:22",
  "session_end": "2026-01-15T14:50:22",
  "messages": [
    {
      "role": "user",
      "content": "안녕하세요"
    },
    {
      "role": "assistant",
      "content": "안녕하세요! 반갑습니다."
    }
  ]
}
```

## 주의사항

### 비대면 실험 진행 시

- ✅ API 키는 미리 설정해두면 참가자는 바로 사용 가능
- ✅ 참가자는 참여자 ID만 입력하면 즉시 시작
- ✅ 대화 기록은 자동으로 저장되어 연구자가 나중에 분석
- ⚠️ API 키는 절대 공개 저장소에 업로드하지 마세요
- ⚠️ `.env` 파일은 `.gitignore`에 포함되어 있습니다

### 비용 관리

- OpenAI API 사용 시 비용이 발생할 수 있습니다
- GPT-3.5-turbo는 상대적으로 저렴하지만, 사용량에 따라 비용 모니터링 권장
- OpenAI 대시보드에서 사용량 확인 가능

## 문제 해결

### API 키 오류
- `.env` 파일에 올바른 API 키가 입력되어 있는지 확인하세요.
- OpenAI 계정에서 API 키가 활성화되어 있는지 확인하세요.

### 세션이 자동으로 종료되지 않음
- 브라우저를 새로고침하면 타이머가 업데이트됩니다.

## 라이선스

연구 목적으로만 사용하세요.
