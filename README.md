<div align="center">
📡 K-POP Comeback Radar
Apple Music Catalog · YouTube · Global News · Naver News · Solar AI
<br>
K-POP 아티스트의 컴백 신호를 한 화면에서 탐색하는  
Streamlit 기반 데이터·AI 대시보드
<br>
![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-Web_App-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Apple](https://img.shields.io/badge/Apple-iTunes_Search-000000?style=for-the-badge&logo=apple&logoColor=white)
![YouTube](https://img.shields.io/badge/YouTube-Data_API-FF0000?style=for-the-badge&logo=youtube&logoColor=white)
![Solar](https://img.shields.io/badge/Upstage-Solar_AI-6C5CE7?style=for-the-badge)
<br>
> 음악 발매 정보, 영상 반응, 국내외 뉴스 화제성을 모아  
> **Comeback Score**와 **AI 분석 인사이트**를 제공하는 학습용 프로젝트입니다.
</div>
---
✨ Project Overview
K-POP Comeback Radar는 여러 공개 API를 결합해  
K-POP 아티스트의 최근 활동과 컴백 신호를 시각적으로 보여주는 웹앱입니다.
사용자는 사이드바에서 아티스트를 선택한 뒤 다음 정보를 확인할 수 있습니다.
영역	제공 정보
🍎 Apple Music Catalog	최신 앨범, 발매일, 트랙 수, 앨범 이미지, Apple Music 링크
🎧 Apple Search Tracks	검색 관련도 기준 트랙, 앨범명, 발매일, 미리듣기
🎬 YouTube Signal	최근 영상, 조회수, 좋아요, 댓글
🌎 Global News	Mediastack 기반 영문권 기사
🇰🇷 Korean News	네이버 검색 API 기반 국내 기사
📈 Comeback Score	발매·영상·뉴스 신호를 조합한 자체 지표
🤖 Solar AI Analyst	수집된 데이터를 바탕으로 한 질의응답
---
🎨 UI Concept
이번 버전은 Apple Music 스타일의 화이트·라벤더 디자인을 중심으로 구성했습니다.
Design Direction
밝은 화이트·라벤더·핑크 그라데이션
Apple 계열 시스템 폰트 우선 적용
반투명 Glassmorphism 카드
KPI 카드 순차 등장 애니메이션
앨범 카드 Hover 인터랙션
모바일 화면 최적화
사이드바와 콘텐츠 영역의 명확한 대비
아티스트 선택창 텍스트는 검정색으로 고정
Color System
용도	컬러
Primary Purple	`#6957D9`
Secondary Pink	`#D94F9A`
Main Text	`#25233A`
Muted Text	`#66647B`
Lavender Background	`#F0EDFF`
Card Background	`rgba(255,255,255,.70)`
---
🧭 Main Experience
```text
┌──────────────────────────────────────────────────────┐
│                K-POP Comeback Radar                  │
│ Apple · YouTube · Global News · Naver · Solar AI    │
└──────────────────────────────────────────────────────┘

┌──────────────┬──────────────┬──────────────┐
│ Apple Albums │ YouTube View │ Global News  │
│      12      │    48.5M     │      10      │
└──────────────┴──────────────┴──────────────┘

┌─────────────────┬──────────────────┬───────────────┐
│ Latest Release  │ YouTube Signal   │ Comeback Score│
│ Album Artwork   │ Recent Videos    │      82       │
└─────────────────┴──────────────────┴───────────────┘

┌──────────────────────────────────────────────────────┐
│ Global News / Korean News                           │
├──────────────────────────────────────────────────────┤
│ Solar AI Analyst Chat                               │
└──────────────────────────────────────────────────────┘
```
---
🛠 Tech Stack
Category	Technology
Frontend / Web App	Streamlit
Language	Python
Data Processing	Pandas
Visualization	Plotly
HTTP Client	Requests
Music Catalog	Apple iTunes Search API
Video Analytics	YouTube Data API v3
Global News	Mediastack API
Korean News	Naver Search API
AI Chat	Upstage Solar API
Deployment	Streamlit Community Cloud
Version Control	GitHub
---
📂 Project Structure
```text
my-kpop-app/
├── main.py
├── requirements.txt
└── README.md
```
---
🚀 Getting Started
1. Repository Clone
```bash
git clone https://github.com/YOUR_GITHUB_ID/YOUR_REPOSITORY.git
cd YOUR_REPOSITORY
```
2. Virtual Environment
macOS / Linux
```bash
python -m venv .venv
source .venv/bin/activate
```
Windows
```bash
python -m venv .venv
.venv\Scripts\activate
```
3. Install Dependencies
```bash
pip install -r requirements.txt
```
4. Run Streamlit
```bash
streamlit run main.py
```
브라우저에서 다음 주소로 실행됩니다.
```text
http://localhost:8501
```
---
📦 requirements.txt
```txt
streamlit>=1.41.0
requests>=2.32.0
pandas>=2.2.0
plotly>=5.24.0
```
---
🔑 API Configuration
Apple iTunes Search API는 별도 키가 필요하지 않습니다.
나머지 API 키는 Streamlit Secrets 또는 로컬 `.streamlit/secrets.toml`에 저장합니다.
`.streamlit/secrets.toml`
```toml
YOUTUBE_API_KEY = "YOUR_YOUTUBE_API_KEY"

MEDIASTACK_API_KEY = "YOUR_MEDIASTACK_API_KEY"

NAVER_CLIENT_ID = "YOUR_NAVER_CLIENT_ID"
NAVER_CLIENT_SECRET = "YOUR_NAVER_CLIENT_SECRET"

SOLAR_API_KEY = "YOUR_SOLAR_API_KEY"
SOLAR_MODEL = "solar-pro3"
```
> API Key는 절대로 `main.py` 또는 공개 GitHub 저장소에 직접 입력하지 마세요.
---
🔌 API Roles
🍎 Apple iTunes Search API
별도 인증키 없이 사용합니다.
```text
https://itunes.apple.com/search
```
활용 데이터:
아티스트명
앨범명
발매일
앨범 이미지
트랙 수
Apple Music 링크
일부 트랙 미리듣기
Apple 검색 결과는 공식 인기 순위가 아니라 검색 관련도 순서입니다.
---
🎬 YouTube Data API
활용 데이터:
최근 업로드 영상
영상 조회수
좋아요 수
댓글 수
채널명
업로드 날짜
YouTube 검색 API는 할당량을 사용하므로  
앱에서는 `st.cache_data`를 적용해 불필요한 반복 호출을 줄였습니다.
---
🌎 Mediastack
활용 데이터:
글로벌 영문 뉴스
기사 제목
출처
발행일
기사 링크
무료 플랜에서는 HTTP 엔드포인트 또는 호출량 제한이 있을 수 있습니다.
---
🇰🇷 Naver Search API
활용 데이터:
국내 최신 뉴스
기사 제목
발행일
원문 링크
요청 헤더:
```text
X-Naver-Client-Id
X-Naver-Client-Secret
```
---
🤖 Upstage Solar
수집된 음악·영상·뉴스 데이터를 기반으로 질문에 답합니다.
예시 질문:
```text
이번 컴백에서 가장 강한 신호는 무엇이야?
국내와 해외 반응의 차이를 분석해줘.
마케팅 관점에서 핵심 시사점을 정리해줘.
YouTube 반응과 뉴스 화제성을 비교해줘.
```
Solar API가 연결되지 않은 경우에는  
앱 내부의 규칙 기반 분석으로 대체됩니다.
---
📈 Comeback Score
Comeback Score는 공식 차트나 매출 지표가 아니라  
본 프로젝트에서 정의한 학습용 자체 지표입니다.
지표	가중치
최신 발매 시점	30%
YouTube 반응	35%
글로벌 뉴스	15%
국내 뉴스	15%
Apple 카탈로그 규모	5%
합계	100%
Score Interpretation
점수	해석
85–100	🔥 초강력 컴백 신호
70–84	🚀 높은 관심도
55–69	✨ 상승 신호 감지
40–54	🌙 관심도 관찰 중
0–39	📡 레이더 탐색 중
Important Note
Apple 카탈로그 검색량은 실제 판매량이나 스트리밍 수가 아닙니다.
YouTube 조회수는 수집 시점의 누적 값입니다.
뉴스 기사량은 API 검색 결과와 무료 플랜 한도에 영향을 받습니다.
Comeback Score는 아티스트 간 공식 비교 지표로 사용하면 안 됩니다.
---
🧪 Demo Mode
API 키가 없거나 호출에 실패해도 앱 전체가 중단되지 않도록  
데모 데이터와 예외 처리 기능을 포함했습니다.
사이드바에서:
```text
데모 모드 강제 사용
```
을 활성화하면 모든 화면을 샘플 데이터로 확인할 수 있습니다.
실데이터 연결 상태는 사이드바에 다음과 같이 표시됩니다.
```text
🟢 Apple Music Catalog
🟢 YouTube
🟢 Mediastack
🟢 네이버 뉴스
🟢 Solar AI
```
---
☁️ Streamlit Cloud Deployment
1. GitHub에 파일 업로드
```text
main.py
requirements.txt
README.md
```
2. Streamlit Community Cloud에서 앱 생성
Repository: 프로젝트 저장소
Branch: `main`
Main file path: `main.py`
3. Secrets 등록
```text
Manage app
→ Settings
→ Secrets
```
Secrets를 저장한 뒤 앱을 재부팅합니다.
```text
Manage app
→ Reboot app
```
---
📱 Responsive Design
모바일 화면에서는 다음 요소가 자동 조정됩니다.
Hero 타이틀 크기 축소
카드 패딩 및 간격 조정
앨범 이미지 축소
KPI 숫자 크기 조정
Hover 효과 비활성화
탭 및 채팅 UI 크기 최적화
---
⚠️ Troubleshooting
Apple 데이터가 검색되지 않을 때
아티스트 영문명이 Apple 카탈로그에 등록된 이름과 다른지 확인
검색 결과가 다른 동명의 아티스트와 섞이는지 확인
`ARTISTS` 딕셔너리의 `apple_query` 값을 수정
YouTube 오류
```text
HTTP 403
quotaExceeded
```
일일 API 할당량 확인
Google Cloud에서 YouTube Data API v3 활성화 여부 확인
API Key 제한 설정 확인
Mediastack 오류
```text
invalid_access_key
usage_limit_reached
https_access_restricted
```
API Key 확인
무료 플랜 호출량 확인
무료 플랜의 HTTP/HTTPS 정책 확인
Naver API 오류
```text
HTTP 401
HTTP 403
```
Client ID와 Client Secret 확인
네이버 개발자센터에서 검색 API가 선택됐는지 확인
애플리케이션 환경 등록 확인
Solar 오류
```text
model_not_found
unauthorized
```
Solar API Key 확인
현재 사용 가능한 모델명 확인
`SOLAR_MODEL` 값을 계정에서 제공되는 모델명으로 변경
---
🔒 Security
다음 파일은 GitHub에 업로드하지 않는 것을 권장합니다.
```gitignore
.streamlit/secrets.toml
.env
.venv/
__pycache__/
*.pyc
```
추천 `.gitignore`:
```gitignore
.streamlit/secrets.toml
.env
.venv/
__pycache__/
*.pyc
.DS_Store
```
---
🗺 Roadmap
현재 버전 이후 확장 가능한 기능:
아티스트 직접 검색
국가별 YouTube 반응 비교
컴백 전후 조회수 추이 저장
발매 일정 캘린더
뉴스 키워드 분석
멀티 아티스트 비교
AI 자동 요약 카드
컴백 알림 기능
---
📌 Disclaimer
이 프로젝트는 API 활용, 데이터 시각화, Streamlit 배포 및  
생성형 AI 연동을 학습하기 위한 개인 프로젝트입니다.
Apple, YouTube, Naver, Mediastack, Upstage 및 각 아티스트·기획사와  
공식적인 제휴 관계가 없습니다.
모든 상표와 콘텐츠의 권리는 각 소유자에게 있습니다.
---
<div align="center">
Built with Python, Streamlit and K-POP Data
K-POP Comeback Radar
🍎 Apple Music Catalog · 🎬 YouTube · 📰 News · 🤖 Solar AI
</div>
