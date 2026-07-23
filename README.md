<div align="center">
📡 K-POP Comeback Radar
Apple Music Catalog · YouTube · Global News · Naver News · Solar AI
<br>
<img src="https://img.shields.io/badge/Apple-iTunes_Search_API-111111?style=for-the-badge&logo=apple&logoColor=white" alt="Apple">
<img src="https://img.shields.io/badge/YouTube-Data_API_v3-FF0033?style=for-the-badge&logo=youtube&logoColor=white" alt="YouTube">
<img src="https://img.shields.io/badge/Streamlit-Web_App-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit">
<br><br>
<img src="https://img.shields.io/badge/Mediastack-Global_News-7456D8?style=flat-square" alt="Mediastack">
<img src="https://img.shields.io/badge/Naver-Korean_News-03C75A?style=flat-square&logo=naver&logoColor=white" alt="Naver">
<img src="https://img.shields.io/badge/Upstage-Solar_AI-E36AA5?style=flat-square" alt="Solar">
<br><br>
K-POP 아티스트의 최신 발매, YouTube 반응, 국내외 뉴스와 AI 분석을  
Apple Music 스타일의 밝은 대시보드에서 확인하는 Streamlit 웹앱
<br>
🌐 Live App
</div>
---
✨ What This App Does
K-POP Comeback Radar는 여러 공개 API의 데이터를 하나의 화면에 모아 아티스트의 컴백 신호를 탐색합니다.
영역	제공 정보
🍎 Apple Catalog	최신 앨범, 발매일, 커버 이미지, 트랙, Apple Music 링크
🎬 YouTube Signal	최근 영상, 조회수, 좋아요, 댓글
🌎 Global News	Mediastack 기반 영문권 기사
🇰🇷 Korean News	네이버 검색 API 기반 국내 기사
📈 Comeback Score	발매·영상·뉴스 신호를 조합한 자체 지표
🤖 Solar Analyst	현재 수집된 데이터를 기반으로 한 AI 질의응답
> 음악 데이터는 Apple iTunes Search API를 사용합니다.  
> 이 버전에는 Spotify API, Spotify Secret, Spotify 화면 문구가 포함되지 않습니다.
---
🎨 UI Concept
이번 버전의 핵심은 Apple Music 스타일의 화이트·라벤더 인터페이스입니다.
Design Highlights
밝은 화이트·라벤더·핑크 그라데이션 배경
Apple 계열 시스템 폰트 우선 적용
반투명 Glassmorphism 카드
KPI 카드 순차 등장 애니메이션
앨범 카드 Hover 상승·확대 효과
모바일 화면 최적화
사이드바 일반 텍스트는 흰색
아티스트 선택창 내부 글씨는 검정색
차트·카드·본문의 컬러 체계 통일
Color Palette
Role	Color
Primary Purple	`#6F5BD6`
Deep Purple	`#4F3DB1`
Accent Pink	`#DD6AA7`
Main Text	`#242238`
Muted Text	`#6D6980`
Lavender	`#EEE7FF`
Light Background	`#FFF9FC`
Glass Card	`rgba(255,255,255,.72)`
Typography
```css
-apple-system,
BlinkMacSystemFont,
"SF Pro Display",
"SF Pro Text",
"Pretendard",
"Noto Sans KR",
"Segoe UI",
sans-serif
```
---
🖥 Screen Structure
```text
┌──────────────────────────────────────────────────────────────────────┐
│ K-POP DATA & AI INTELLIGENCE                                        │
│ K-POP Comeback Radar                                                │
│ Apple · YouTube · Global News · Korean News · Solar AI             │
└──────────────────────────────────────────────────────────────────────┘

┌──────────────┬──────────────┬──────────────┬────────────┬────────────┐
│ Apple Albums │ Apple Tracks │ YouTube View │ Global News│ Korean News│
└──────────────┴──────────────┴──────────────┴────────────┴────────────┘

┌─────────────────────┬─────────────────────┬──────────────────────────┐
│ Latest Apple Release│ YouTube Signal      │ Comeback Score           │
│ Album Artwork       │ Recent Videos       │ Radar Chart              │
│ Release Information │ Views / Likes       │ Signal Interpretation    │
└─────────────────────┴─────────────────────┴──────────────────────────┘

┌──────────────────────────────────────────────────────────────────────┐
│ Global News / Korean News                                           │
├──────────────────────────────────────────────────────────────────────┤
│ Radar Interpretation                                                │
├──────────────────────────────────────────────────────────────────────┤
│ Solar AI Analyst Chat                                               │
└──────────────────────────────────────────────────────────────────────┘
```
---
🖼 Add a Real Screenshot
앱 화면을 캡처한 뒤 저장소에 다음 경로로 업로드하세요.
```text
assets/kpop-radar-preview.png
```
README에 아래 코드를 추가하면 실제 앱 화면이 표시됩니다.
```html
<p align="center">
  <img
    src="assets/kpop-radar-preview.png"
    width="100%"
    alt="K-POP Comeback Radar Preview"
  >
</p>
```
권장 캡처:
데스크톱 브라우저 폭 1440px 이상
Hero 영역부터 Comeback Score까지 포함
사이드바를 펼친 상태
실제 Apple 앨범 이미지가 표시된 상태
---
🍎 Apple-Only Music Data
음악 카탈로그는 다음 엔드포인트를 사용합니다.
```text
https://itunes.apple.com/search
```
Data Fields
아티스트명
앨범명
발매일
앨범 커버
트랙 수
Apple Music 링크
트랙 미리듣기
장르
검색된 앨범·트랙 수
Apple 검색 결과는 공식 인기 순위가 아니라 검색 관련도 순서입니다.
정상 배포된 최종 버전은 앱 하단에 다음 문구가 표시됩니다.
```text
APPLE-ONLY BUILD 2026-07-23
```
---
📊 Comeback Score
Comeback Score는 공식 차트가 아니라 프로젝트에서 정의한 학습용 지표입니다.
Signal	Weight
발매 최신성	30%
YouTube 반응	35%
글로벌 뉴스	15%
국내 뉴스	15%
Apple 카탈로그	5%
Total	100%
Score Guide
Score	Meaning
85–100	🔥 초강력 컴백 신호
70–84	🚀 높은 관심도
55–69	✨ 상승 신호 감지
40–54	🌙 관심도 관찰 중
0–39	📡 레이더 탐색 중
---
🛠 Tech Stack
Category	Technology
Web App	Streamlit
Language	Python
Data Processing	Pandas
Visualization	Plotly
HTTP	Requests
Music	Apple iTunes Search API
Video	YouTube Data API v3
Global News	Mediastack
Korean News	Naver Search API
AI	Upstage Solar
Deployment	Streamlit Community Cloud
Version Control	GitHub
---
📁 Project Structure
```text
my-kpop-app/
├── main.py
├── requirements.txt
├── README.md
└── assets/
    └── kpop-radar-preview.png
```
---
🚀 Local Setup
1. Clone
```bash
git clone https://github.com/YOUR_GITHUB_ID/YOUR_REPOSITORY.git
cd YOUR_REPOSITORY
```
2. Create Virtual Environment
Windows
```bash
python -m venv .venv
.venv\Scripts\activate
```
macOS / Linux
```bash
python -m venv .venv
source .venv/bin/activate
```
3. Install
```bash
pip install -r requirements.txt
```
4. Run
```bash
streamlit run main.py
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
🔑 Streamlit Secrets
Apple iTunes Search API는 별도 키가 필요하지 않습니다.
```toml
YOUTUBE_API_KEY = "YOUR_YOUTUBE_API_KEY"

MEDIASTACK_API_KEY = "YOUR_MEDIASTACK_API_KEY"

NAVER_CLIENT_ID = "YOUR_NAVER_CLIENT_ID"
NAVER_CLIENT_SECRET = "YOUR_NAVER_CLIENT_SECRET"

SOLAR_API_KEY = "YOUR_SOLAR_API_KEY"
SOLAR_MODEL = "solar-pro3"
```
로컬에서는 다음 파일에 저장합니다.
```text
.streamlit/secrets.toml
```
> API 키는 `main.py`, `README.md`, 공개 GitHub 저장소에 직접 입력하지 마세요.
---
🧪 Demo Mode
일부 API 키가 없거나 호출이 실패해도 앱 전체가 중단되지 않도록 데모 데이터가 제공됩니다.
사이드바에서:
```text
데모 모드 강제 사용
```
을 활성화하면 샘플 데이터로 전체 UI를 확인할 수 있습니다.
연결 상태 예시:
```text
🟢 Apple Music Catalog
🟢 YouTube
🟢 Mediastack
🟢 네이버 뉴스
🟢 Solar AI
```
---
☁️ Streamlit Cloud Deployment
Deploy Settings
```text
Repository: GitHub 저장소
Branch: main
Main file path: main.py
```
Secrets
```text
Manage app
→ Settings
→ Secrets
```
Reboot
```text
Manage app
→ Reboot app
```
Confirm the Correct Build
화면 하단에 다음 문구가 보여야 합니다.
```text
APPLE-ONLY BUILD 2026-07-23
```
보이지 않는다면 다음 항목을 확인하세요.
GitHub에 Apple 최종 파일이 실제로 커밋됐는지
배포 Branch가 올바른지
Main file path가 `main.py`인지
다른 폴더의 오래된 파일을 실행 중이지 않은지
---
📱 Responsive Design
모바일에서는 다음 UI가 자동 조정됩니다.
Hero 타이틀 크기
본문 줄 간격
앨범 커버 크기
카드 패딩과 간격
KPI 숫자 크기
뉴스 탭 크기
채팅 카드 크기
Hover 이동 효과 비활성화
---
🧯 Troubleshooting
이전 Spotify 화면이 표시될 때
GitHub의 `main.py`에서 아래 문자열을 검색합니다.
```text
Spotify
SPOTIFY_API_URL
SPOTIFY_CLIENT_ID
SPOTIFY_CLIENT_SECRET
get_spotify_data
```
최종 Apple 전용 파일에서는 모두 0건이어야 합니다.
반드시 존재해야 하는 문자열:
```text
ITUNES_SEARCH_URL
get_apple_music_data
MEDIASTACK_API_URL
APPLE-ONLY BUILD 2026-07-23
```
Apple Image Quality
고해상도 앨범 이미지는 다음 방식으로 변환합니다.
```python
artwork_high_res = artwork.replace(
    "100x100bb",
    "600x600bb",
)
```
YouTube 403
YouTube Data API v3 활성화 여부
API Key 제한
일일 할당량
Mediastack Error
API Key
무료 플랜 호출량
HTTP/HTTPS 플랜 제한
Naver 401 / 403
Client ID와 Client Secret
검색 API 선택 여부
애플리케이션 환경 등록
Solar Error
API Key
사용 가능한 모델명
`SOLAR_MODEL` 값
---
🔒 Security
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
자유 아티스트 검색
아티스트 비교
발매 일정 캘린더
컴백 전후 YouTube 추이
국가별 뉴스 비교
뉴스 키워드 분석
AI 자동 요약 카드
컴백 알림
---
⚠️ Disclaimer
이 프로젝트는 API 활용, 데이터 시각화, Streamlit 배포와 생성형 AI 연동을 연습하기 위한 개인 프로젝트입니다.
Apple, YouTube, Naver, Mediastack, Upstage, 아티스트 및 기획사와 공식적인 제휴 관계가 없습니다.
모든 상표와 콘텐츠의 권리는 각 소유자에게 있습니다.
---
<div align="center">
📡 K-POP Comeback Radar
🍎 Apple Catalog · 🎬 YouTube · 📰 Global & Korean News · 🤖 Solar AI
<br>
`APPLE-ONLY BUILD`
</div>
