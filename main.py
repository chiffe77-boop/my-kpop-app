from __future__ import annotations

import html
import math
import re
from datetime import datetime, timezone
from typing import Any

import pandas as pd
import plotly.express as px
import requests
import streamlit as st


# =========================================================
# 1. PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="K-POP Comeback Radar",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# 2. API ENDPOINTS / ARTISTS
# =========================================================

ITUNES_SEARCH_URL = "https://itunes.apple.com/search"
YOUTUBE_API_URL = "https://www.googleapis.com/youtube/v3"
MEDIASTACK_API_URL = "http://api.mediastack.com/v1/news"
NAVER_NEWS_API_URL = "https://openapi.naver.com/v1/search/news.json"
SOLAR_CHAT_API_URL = "https://api.upstage.ai/v1/solar/chat/completions"

ARTISTS: dict[str, dict[str, str]] = {
    "aespa": {
        "apple_query": "aespa",
        "youtube_query": "aespa official",
        "global_news_query": "aespa",
        "naver_news_query": "에스파",
        "emoji": "🪩",
    },
    "BLACKPINK": {
        "apple_query": "BLACKPINK",
        "youtube_query": "BLACKPINK official",
        "global_news_query": "BLACKPINK",
        "naver_news_query": "블랙핑크",
        "emoji": "🖤",
    },
    "BTS": {
        "apple_query": "BTS",
        "youtube_query": "BTS official BANGTANTV",
        "global_news_query": "BTS K-pop",
        "naver_news_query": "방탄소년단",
        "emoji": "💜",
    },
    "IVE": {
        "apple_query": "IVE",
        "youtube_query": "IVE official",
        "global_news_query": "IVE K-pop",
        "naver_news_query": "아이브",
        "emoji": "✨",
    },
    "LE SSERAFIM": {
        "apple_query": "LE SSERAFIM",
        "youtube_query": "LE SSERAFIM official",
        "global_news_query": "LE SSERAFIM",
        "naver_news_query": "르세라핌",
        "emoji": "🔥",
    },
    "NCT DREAM": {
        "apple_query": "NCT DREAM",
        "youtube_query": "NCT DREAM official",
        "global_news_query": "NCT DREAM",
        "naver_news_query": "엔시티 드림",
        "emoji": "💚",
    },
    "NewJeans": {
        "apple_query": "NewJeans",
        "youtube_query": "NewJeans official",
        "global_news_query": "NewJeans",
        "naver_news_query": "뉴진스",
        "emoji": "🐰",
    },
    "RIIZE": {
        "apple_query": "RIIZE",
        "youtube_query": "RIIZE official",
        "global_news_query": "RIIZE K-pop",
        "naver_news_query": "라이즈",
        "emoji": "🌅",
    },
    "SEVENTEEN": {
        "apple_query": "SEVENTEEN",
        "youtube_query": "SEVENTEEN official",
        "global_news_query": "SEVENTEEN K-pop",
        "naver_news_query": "세븐틴",
        "emoji": "💎",
    },
    "Stray Kids": {
        "apple_query": "Stray Kids",
        "youtube_query": "Stray Kids official",
        "global_news_query": "Stray Kids",
        "naver_news_query": "스트레이 키즈",
        "emoji": "⚡",
    },
}


# =========================================================
# 3. BRIGHT UI CSS
# =========================================================

st.markdown(
    """
    <style>
        :root {
            --ink: #242238;
            --muted: #6d6980;
            --purple: #6f5bd6;
            --purple-dark: #4f3db1;
            --pink: #dd6aa7;
            --lavender: #eeeaff;
            --glass: rgba(255, 255, 255, .72);
            --glass-border: rgba(255, 255, 255, .84);
            --soft-shadow: 0 14px 38px rgba(88, 72, 150, .10);
        }

        html, body, [class*="css"] {
            font-family:
                -apple-system,
                BlinkMacSystemFont,
                "SF Pro Display",
                "SF Pro Text",
                "Pretendard",
                "Noto Sans KR",
                "Segoe UI",
                sans-serif;
            -webkit-font-smoothing: antialiased;
            text-rendering: optimizeLegibility;
        }

        .stApp {
            min-height: 100vh;
            color: var(--ink);
            background:
                radial-gradient(circle at 7% 6%, rgba(219, 211, 255, .78), transparent 29%),
                radial-gradient(circle at 94% 5%, rgba(255, 218, 239, .72), transparent 30%),
                linear-gradient(180deg, #fffefe 0%, #f9f8ff 45%, #fff9fc 100%);
        }

        .block-container {
            max-width: 1420px;
            padding-top: 1.6rem;
            padding-bottom: 3rem;
        }

        [data-testid="stSidebar"] {
            background:
                radial-gradient(circle at 30% 0%, rgba(255,255,255,.14), transparent 26%),
                linear-gradient(180deg, #5544bd 0%, #6653cb 50%, #7b5fc9 100%);
            border-right: 1px solid rgba(255,255,255,.22);
        }

        [data-testid="stSidebar"] label,
        [data-testid="stSidebar"] p,
        [data-testid="stSidebar"] h1,
        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] h3,
        [data-testid="stSidebar"] .stMarkdown span,
        [data-testid="stSidebar"] .stCaptionContainer span {
            color: #ffffff !important;
        }

        [data-testid="stSidebar"] .stButton > button {
            color: var(--purple-dark) !important;
            background: #ffffff;
            border: 0;
            border-radius: 13px;
            font-weight: 800;
            box-shadow: 0 8px 20px rgba(44, 31, 111, .18);
        }

        [data-testid="stSidebar"] .stButton > button * {
            color: var(--purple-dark) !important;
        }

        [data-testid="stSidebar"] [data-baseweb="select"] > div {
            background: #ffffff !important;
            border-color: rgba(255,255,255,.92) !important;
            border-radius: 12px;
        }

        [data-testid="stSidebar"] [data-baseweb="select"] input,
        [data-testid="stSidebar"] [data-baseweb="select"] div,
        [data-testid="stSidebar"] [data-baseweb="select"] span {
            color: #111111 !important;
            caret-color: #111111 !important;
        }

        [data-testid="stSidebar"] [data-baseweb="select"] svg {
            color: #111111 !important;
            fill: #111111 !important;
        }

        div[role="listbox"] {
            background: #ffffff !important;
        }

        div[role="listbox"] *,
        div[role="option"],
        div[role="option"] * {
            color: #111111 !important;
        }

        div[role="option"]:hover,
        div[role="option"][aria-selected="true"] {
            color: #111111 !important;
            background: #eeeaff !important;
        }

        .hero {
            position: relative;
            overflow: hidden;
            padding: 35px 37px;
            margin-bottom: 24px;
            border-radius: 30px;
            border: 1px solid rgba(255,255,255,.36);
            background:
                radial-gradient(circle at 84% 14%, rgba(255,255,255,.42), transparent 25%),
                linear-gradient(125deg, #7564df 0%, #a56bd4 52%, #df79ad 100%);
            box-shadow: 0 22px 54px rgba(94, 72, 172, .22);
        }

        .hero::after {
            content: "";
            position: absolute;
            width: 245px;
            height: 245px;
            right: -62px;
            bottom: -105px;
            border-radius: 50%;
            border: 40px solid rgba(255,255,255,.12);
        }

        .eyebrow {
            position: relative;
            z-index: 1;
            color: rgba(255,255,255,.88);
            font-size: .77rem;
            font-weight: 800;
            letter-spacing: .18em;
            text-transform: uppercase;
            margin-bottom: 9px;
        }

        .hero-title {
            position: relative;
            z-index: 1;
            color: #ffffff !important;
            font-size: clamp(2.4rem, 4.8vw, 4.65rem);
            line-height: 1.02;
            font-weight: 900;
            letter-spacing: -.052em;
            text-shadow: 0 4px 20px rgba(55, 34, 120, .22);
            margin: 0;
        }

        .hero-subtitle {
            position: relative;
            z-index: 1;
            max-width: 900px;
            margin-top: 15px;
            color: rgba(255,255,255,.96);
            font-size: 1.02rem;
            line-height: 1.68;
            font-weight: 500;
        }

        .badge {
            position: relative;
            z-index: 1;
            display: inline-block;
            padding: 5px 10px;
            margin: 3px 4px 2px 0;
            color: #ffffff;
            font-size: .72rem;
            font-weight: 800;
            border-radius: 999px;
            background: rgba(255,255,255,.18);
            border: 1px solid rgba(255,255,255,.36);
        }

        .section-title {
            color: #302b52;
            font-size: 1.35rem;
            font-weight: 850;
            letter-spacing: -.025em;
            margin: 15px 0;
        }

        .muted {
            color: var(--muted);
            font-size: .90rem;
            line-height: 1.58;
        }

        .glass-card,
        .album-card,
        .news-card,
        div[data-testid="stMetric"],
        div[data-testid="stChatMessage"] {
            backdrop-filter: blur(18px) saturate(150%);
            -webkit-backdrop-filter: blur(18px) saturate(150%);
        }

        .glass-card {
            height: 100%;
            padding: 21px;
            border-radius: 22px;
            background: var(--glass);
            border: 1px solid var(--glass-border);
            box-shadow:
                var(--soft-shadow),
                inset 0 1px 0 rgba(255,255,255,.88);
        }

        .album-card {
            display: flex;
            gap: 18px;
            align-items: center;
            padding: 19px;
            margin-bottom: 14px;
            border-radius: 23px;
            background: rgba(255,255,255,.74);
            border: 1px solid rgba(255,255,255,.86);
            box-shadow:
                0 14px 34px rgba(83,68,145,.10),
                inset 0 1px 0 rgba(255,255,255,.90);
            transition:
                transform .28s cubic-bezier(.2,.8,.2,1),
                box-shadow .28s ease,
                border-color .28s ease;
            will-change: transform;
        }

        .album-card:hover {
            transform: translateY(-5px) scale(1.012);
            border-color: rgba(111,86,215,.30);
            box-shadow:
                0 22px 48px rgba(83,68,145,.17),
                inset 0 1px 0 rgba(255,255,255,.96);
        }

        .album-cover {
            width: 120px;
            height: 120px;
            min-width: 120px;
            border-radius: 17px;
            object-fit: cover;
            background: linear-gradient(135deg, #e8e1ff, #ffdceb);
            box-shadow: 0 9px 22px rgba(86,66,150,.14);
            transition:
                transform .28s cubic-bezier(.2,.8,.2,1),
                box-shadow .28s ease;
        }

        .album-card:hover .album-cover {
            transform: scale(1.035);
            box-shadow: 0 15px 30px rgba(86,66,150,.20);
        }

        .album-name {
            margin: 7px 0;
            color: #282342;
            font-size: 1.14rem;
            font-weight: 900;
            line-height: 1.35;
        }

        .score-card {
            padding: 28px 19px;
            text-align: center;
            border-radius: 23px;
            background:
                radial-gradient(circle at 50% 0%, rgba(255,255,255,.82), transparent 36%),
                linear-gradient(145deg, #eeeaff 0%, #ffeaf5 100%);
            border: 1px solid rgba(111,91,205,.18);
            box-shadow: 0 13px 32px rgba(92,70,166,.11);
        }

        .score-number {
            margin-top: 5px;
            color: #674fca;
            font-size: 3.9rem;
            line-height: 1;
            font-weight: 950;
        }

        @keyframes metricRise {
            from {
                opacity: 0;
                transform: translateY(12px) scale(.985);
            }
            to {
                opacity: 1;
                transform: translateY(0) scale(1);
            }
        }

        div[data-testid="stMetric"] {
            padding: 17px;
            border-radius: 20px;
            background: rgba(255,255,255,.73);
            border: 1px solid rgba(255,255,255,.86);
            box-shadow:
                0 11px 30px rgba(83,68,140,.09),
                inset 0 1px 0 rgba(255,255,255,.92);
            animation: metricRise .62s cubic-bezier(.2,.8,.2,1) both;
            transition: transform .22s ease, box-shadow .22s ease;
        }

        div[data-testid="stMetric"]:hover {
            transform: translateY(-3px);
            box-shadow:
                0 17px 36px rgba(83,68,140,.14),
                inset 0 1px 0 rgba(255,255,255,.96);
        }

        div[data-testid="stMetric"] label,
        div[data-testid="stMetric"] [data-testid="stMetricLabel"] {
            color: #6b6880 !important;
        }

        div[data-testid="stMetric"] [data-testid="stMetricValue"] {
            color: #2f294f !important;
        }

        div[data-testid="stHorizontalBlock"] > div:nth-child(1) div[data-testid="stMetric"] { animation-delay: .04s; }
        div[data-testid="stHorizontalBlock"] > div:nth-child(2) div[data-testid="stMetric"] { animation-delay: .10s; }
        div[data-testid="stHorizontalBlock"] > div:nth-child(3) div[data-testid="stMetric"] { animation-delay: .16s; }
        div[data-testid="stHorizontalBlock"] > div:nth-child(4) div[data-testid="stMetric"] { animation-delay: .22s; }
        div[data-testid="stHorizontalBlock"] > div:nth-child(5) div[data-testid="stMetric"] { animation-delay: .28s; }

        .news-card {
            padding: 16px 18px;
            margin-bottom: 11px;
            border-radius: 18px;
            background: rgba(255,255,255,.70);
            border: 1px solid rgba(255,255,255,.84);
            box-shadow: 0 10px 26px rgba(87,70,145,.08);
        }

        .news-title {
            color: #302a54;
            font-size: .99rem;
            font-weight: 850;
            line-height: 1.48;
            text-decoration: none;
        }

        .news-title:hover {
            color: var(--purple);
        }

        .news-meta {
            margin-top: 8px;
            color: #77738b;
            font-size: .78rem;
        }

        div[data-testid="stChatMessage"] {
            padding: 9px 13px;
            color: #2d2943;
            border-radius: 17px;
            background: rgba(255,255,255,.74);
            border: 1px solid rgba(255,255,255,.84);
        }

        div[data-testid="stChatMessage"] * {
            color: #2d2943;
        }

        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
        }

        .stTabs [data-baseweb="tab"] {
            padding: 8px 16px;
            border-radius: 12px;
            background: rgba(255,255,255,.72);
        }

        .stTabs [aria-selected="true"] {
            color: #ffffff !important;
            background: var(--purple) !important;
        }

        .stTabs [aria-selected="true"] * {
            color: #ffffff !important;
        }

        .stAlert {
            border-radius: 16px;
        }

        @media (max-width: 700px) {
            .block-container {
                padding: .85rem .9rem 2rem;
            }

            .hero {
                padding: 23px 19px;
                margin-bottom: 18px;
                border-radius: 22px;
            }

            .eyebrow {
                font-size: .68rem;
                letter-spacing: .14em;
            }

            .hero-title {
                font-size: clamp(2.05rem, 11vw, 2.55rem);
                line-height: 1.05;
                letter-spacing: -.045em;
            }

            .hero-subtitle {
                font-size: .91rem;
                line-height: 1.58;
            }

            .section-title {
                margin: 12px 0;
                font-size: 1.15rem;
            }

            .album-card {
                align-items: flex-start;
                gap: 12px;
                padding: 14px;
                border-radius: 19px;
            }

            .album-card:hover {
                transform: none;
            }

            .album-cover {
                width: 86px;
                height: 86px;
                min-width: 86px;
                border-radius: 14px;
            }

            .album-name {
                font-size: 1rem;
            }

            .muted {
                font-size: .82rem;
            }

            div[data-testid="stMetric"] {
                padding: 13px;
                border-radius: 16px;
            }

            div[data-testid="stMetric"] [data-testid="stMetricValue"] {
                font-size: 1.28rem !important;
            }

            .score-card {
                padding: 22px 15px;
                border-radius: 19px;
            }

            .score-number {
                font-size: 3rem;
            }

            div[data-testid="stChatMessage"] {
                padding: 8px 10px;
            }

            .stTabs [data-baseweb="tab"] {
                padding: 7px 11px;
                font-size: .86rem;
            }
        }

        @media (max-width: 420px) {
            .hero-title {
                font-size: 2rem;
            }

            .hero-subtitle {
                font-size: .86rem;
            }

            .album-cover {
                width: 76px;
                height: 76px;
                min-width: 76px;
            }

            .album-card {
                gap: 10px;
                padding: 12px;
            }
        }

        @media (prefers-reduced-motion: reduce) {
            *, *::before, *::after {
                animation-duration: .01ms !important;
                animation-iteration-count: 1 !important;
                transition-duration: .01ms !important;
                scroll-behavior: auto !important;
            }
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# 4. HELPERS
# =========================================================

def get_secret(name: str, default: str = "") -> str:
    try:
        return str(st.secrets.get(name, default)).strip()
    except Exception:
        return default


def safe_request(
    method: str,
    url: str,
    *,
    headers: dict[str, str] | None = None,
    params: dict[str, Any] | None = None,
    json_body: dict[str, Any] | None = None,
    timeout: int = 20,
) -> dict[str, Any]:
    try:
        response = requests.request(
            method=method,
            url=url,
            headers=headers,
            params=params,
            json=json_body,
            timeout=timeout,
        )
        response.raise_for_status()
        return response.json()

    except requests.exceptions.Timeout as exc:
        raise RuntimeError("API 응답 시간이 초과되었습니다.") from exc

    except requests.exceptions.HTTPError as exc:
        status = exc.response.status_code if exc.response is not None else "unknown"
        try:
            detail = exc.response.json()
        except Exception:
            detail = exc.response.text[:400] if exc.response is not None else ""
        raise RuntimeError(f"HTTP {status}: {detail}") from exc

    except requests.exceptions.RequestException as exc:
        raise RuntimeError(f"네트워크 요청 실패: {exc}") from exc


def escape_text(value: Any) -> str:
    return html.escape(str(value or ""))


def strip_html_tags(value: str | None) -> str:
    if not value:
        return ""
    return html.unescape(re.sub(r"<[^>]+>", "", value)).strip()


def parse_datetime(value: str | None) -> datetime | None:
    if not value:
        return None

    formats = (None, "%a, %d %b %Y %H:%M:%S %z", "%Y-%m-%d")

    for date_format in formats:
        try:
            parsed = (
                datetime.fromisoformat(value.replace("Z", "+00:00"))
                if date_format is None
                else datetime.strptime(value, date_format)
            )
            if parsed.tzinfo is None:
                parsed = parsed.replace(tzinfo=timezone.utc)
            return parsed
        except (ValueError, TypeError):
            continue

    return None


def format_date(value: str | None) -> str:
    parsed = parse_datetime(value)
    return parsed.astimezone().strftime("%Y.%m.%d") if parsed else "-"


def days_since(value: str | None) -> int | None:
    parsed = parse_datetime(value)
    if not parsed:
        return None
    return max((datetime.now(timezone.utc) - parsed.astimezone(timezone.utc)).days, 0)


def format_number(value: int | float | str | None) -> str:
    try:
        number = float(value or 0)
    except (TypeError, ValueError):
        return "-"

    if number >= 1_000_000_000:
        return f"{number / 1_000_000_000:.1f}B"
    if number >= 1_000_000:
        return f"{number / 1_000_000:.1f}M"
    if number >= 1_000:
        return f"{number / 1_000:.1f}K"
    return f"{int(number):,}"


def normalize_youtube_views(value: int | float | None) -> float:
    try:
        views = max(float(value or 0), 0)
    except (TypeError, ValueError):
        views = 0
    return min(math.log10(views + 1) / 8 * 100, 100) if views else 0.0


def freshness_score(release_date: str | None) -> float:
    age = days_since(release_date)
    if age is None:
        return 0.0
    if age <= 7:
        return 100.0
    if age <= 30:
        return 90.0
    if age <= 60:
        return 75.0
    if age <= 90:
        return 60.0
    if age <= 180:
        return 40.0
    if age <= 365:
        return 20.0
    return 5.0


def score_label(score: float) -> str:
    if score >= 85:
        return "🔥 초강력 컴백 신호"
    if score >= 70:
        return "🚀 높은 관심도"
    if score >= 55:
        return "✨ 상승 신호 감지"
    if score >= 40:
        return "🌙 관심도 관찰 중"
    return "📡 레이더 탐색 중"


def artist_name_matches(result_artist: str, target_artist: str) -> bool:
    result = re.sub(r"[^a-z0-9가-힣]", "", result_artist.casefold())
    target = re.sub(r"[^a-z0-9가-힣]", "", target_artist.casefold())
    return result == target or target in result or result in target


# =========================================================
# 5. APPLE ITUNES SEARCH API
# =========================================================

@st.cache_data(ttl=1800, show_spinner=False)
def get_apple_music_data(artist_query: str) -> dict[str, Any]:
    album_result = safe_request(
        "GET",
        ITUNES_SEARCH_URL,
        params={
            "term": artist_query,
            "country": "KR",
            "media": "music",
            "entity": "album",
            "attribute": "artistTerm",
            "limit": 50,
        },
    )

    track_result = safe_request(
        "GET",
        ITUNES_SEARCH_URL,
        params={
            "term": artist_query,
            "country": "KR",
            "media": "music",
            "entity": "musicTrack",
            "attribute": "artistTerm",
            "limit": 50,
        },
    )

    raw_albums = album_result.get("results", [])
    raw_tracks = track_result.get("results", [])

    albums = [
        item for item in raw_albums
        if artist_name_matches(item.get("artistName", ""), artist_query)
    ]
    tracks = [
        item for item in raw_tracks
        if artist_name_matches(item.get("artistName", ""), artist_query)
    ]

    if not albums and not tracks:
        raise RuntimeError("Apple 카탈로그에서 아티스트 데이터를 찾지 못했습니다.")

    unique_albums: list[dict[str, Any]] = []
    seen_album_ids: set[str] = set()

    for album in albums:
        key = str(album.get("collectionId") or album.get("collectionName", "")).strip()
        if key and key not in seen_album_ids:
            seen_album_ids.add(key)
            unique_albums.append(album)

    unique_albums.sort(
        key=lambda item: item.get("releaseDate", ""),
        reverse=True,
    )

    latest = unique_albums[0] if unique_albums else {}

    # 검색 결과 순서는 Apple의 관련도 순서이므로 '인기도'로 표현하지 않습니다.
    selected_tracks = tracks[:10]

    artwork = latest.get("artworkUrl100", "")
    artwork_high_res = artwork.replace("100x100bb", "600x600bb") if artwork else ""

    return {
        "artist": {
            "name": (
                latest.get("artistName")
                or (selected_tracks[0].get("artistName") if selected_tracks else artist_query)
            ),
            "genre": (
                latest.get("primaryGenreName")
                or (selected_tracks[0].get("primaryGenreName") if selected_tracks else "K-Pop")
            ),
            "catalog_albums": len(unique_albums),
            "catalog_tracks": len(tracks),
            "artist_url": latest.get("artistViewUrl", ""),
        },
        "latest_album": {
            "name": latest.get("collectionName", "앨범 정보 없음"),
            "release_date": latest.get("releaseDate", ""),
            "album_type": latest.get("collectionType", "Album"),
            "total_tracks": latest.get("trackCount", 0),
            "image": artwork_high_res,
            "apple_url": latest.get("collectionViewUrl", ""),
            "copyright": latest.get("copyright", ""),
        },
        "tracks": [
            {
                "name": track.get("trackName", ""),
                "album": track.get("collectionName", ""),
                "release_date": track.get("releaseDate", ""),
                "duration_ms": track.get("trackTimeMillis", 0),
                "preview_url": track.get("previewUrl", ""),
                "apple_url": track.get("trackViewUrl", ""),
                "track_number": track.get("trackNumber", 0),
            }
            for track in selected_tracks
        ],
        "albums": [
            {
                "name": album.get("collectionName", ""),
                "release_date": album.get("releaseDate", ""),
                "track_count": album.get("trackCount", 0),
                "apple_url": album.get("collectionViewUrl", ""),
            }
            for album in unique_albums[:10]
        ],
    }


# =========================================================
# 6. YOUTUBE
# =========================================================

@st.cache_data(ttl=1800, show_spinner=False)
def get_youtube_data(search_query: str, api_key: str) -> list[dict[str, Any]]:
    search_result = safe_request(
        "GET",
        f"{YOUTUBE_API_URL}/search",
        params={
            "part": "snippet",
            "q": search_query,
            "type": "video",
            "order": "date",
            "maxResults": 8,
            "key": api_key,
        },
    )

    video_ids = [
        item.get("id", {}).get("videoId")
        for item in search_result.get("items", [])
        if item.get("id", {}).get("videoId")
    ]

    if not video_ids:
        return []

    detail_result = safe_request(
        "GET",
        f"{YOUTUBE_API_URL}/videos",
        params={
            "part": "snippet,statistics",
            "id": ",".join(video_ids),
            "key": api_key,
        },
    )

    videos: list[dict[str, Any]] = []

    for item in detail_result.get("items", []):
        snippet = item.get("snippet", {})
        statistics = item.get("statistics", {})
        thumbnails = snippet.get("thumbnails", {})
        video_id = item.get("id", "")

        videos.append(
            {
                "video_id": video_id,
                "title": html.unescape(snippet.get("title", "")),
                "published_at": snippet.get("publishedAt", ""),
                "channel_title": snippet.get("channelTitle", ""),
                "thumbnail": (
                    thumbnails.get("high", {}).get("url")
                    or thumbnails.get("medium", {}).get("url")
                    or thumbnails.get("default", {}).get("url")
                    or ""
                ),
                "views": int(statistics.get("viewCount", 0)),
                "likes": int(statistics.get("likeCount", 0)),
                "comments": int(statistics.get("commentCount", 0)),
                "url": f"https://www.youtube.com/watch?v={video_id}",
            }
        )

    videos.sort(key=lambda x: x.get("published_at", ""), reverse=True)
    return videos


# =========================================================
# 7. MEDIASTACK
# =========================================================

@st.cache_data(ttl=1800, show_spinner=False)
def get_global_news(query: str, api_key: str) -> list[dict[str, Any]]:
    result = safe_request(
        "GET",
        MEDIASTACK_API_URL,
        params={
            "access_key": api_key,
            "keywords": query,
            "languages": "en",
            "sort": "published_desc",
            "limit": 10,
            "offset": 0,
        },
    )

    if result.get("error"):
        error = result["error"]
        raise RuntimeError(
            f"{error.get('code', 'unknown_error')}: "
            f"{error.get('message', 'Mediastack API 오류')}"
        )

    return [
        {
            "title": article.get("title", ""),
            "description": article.get("description", ""),
            "source": article.get("source", ""),
            "published_at": article.get("published_at", ""),
            "url": article.get("url", ""),
            "image": article.get("image", ""),
            "channel": "Global",
        }
        for article in result.get("data", [])
        if article.get("title") and article.get("url")
    ]


# =========================================================
# 8. NAVER NEWS
# =========================================================

@st.cache_data(ttl=1800, show_spinner=False)
def get_naver_news(
    query: str,
    client_id: str,
    client_secret: str,
) -> list[dict[str, Any]]:
    result = safe_request(
        "GET",
        NAVER_NEWS_API_URL,
        headers={
            "X-Naver-Client-Id": client_id,
            "X-Naver-Client-Secret": client_secret,
        },
        params={
            "query": query,
            "display": 10,
            "start": 1,
            "sort": "date",
        },
    )

    return [
        {
            "title": strip_html_tags(item.get("title")),
            "description": strip_html_tags(item.get("description")),
            "source": "네이버 뉴스",
            "published_at": item.get("pubDate", ""),
            "url": item.get("originallink") or item.get("link", ""),
            "channel": "Korea",
        }
        for item in result.get("items", [])
    ]


# =========================================================
# 9. DEMO DATA
# =========================================================

def get_demo_bundle(artist_name: str) -> dict[str, Any]:
    today = datetime.now(timezone.utc).isoformat()

    return {
        "apple": {
            "artist": {
                "name": artist_name,
                "genre": "K-Pop",
                "catalog_albums": 12,
                "catalog_tracks": 42,
                "artist_url": "",
            },
            "latest_album": {
                "name": f"{artist_name} Demo Album",
                "release_date": today,
                "album_type": "Album",
                "total_tracks": 8,
                "image": "",
                "apple_url": "",
                "copyright": "",
            },
            "tracks": [
                {
                    "name": "Demo Track A",
                    "album": "Demo Album",
                    "release_date": today,
                    "duration_ms": 192000,
                    "preview_url": "",
                    "apple_url": "",
                    "track_number": 1,
                },
                {
                    "name": "Demo Track B",
                    "album": "Demo Album",
                    "release_date": today,
                    "duration_ms": 205000,
                    "preview_url": "",
                    "apple_url": "",
                    "track_number": 2,
                },
                {
                    "name": "Demo Track C",
                    "album": "Demo Album",
                    "release_date": today,
                    "duration_ms": 186000,
                    "preview_url": "",
                    "apple_url": "",
                    "track_number": 3,
                },
            ],
            "albums": [],
        },
        "youtube": [
            {
                "video_id": "demo1",
                "title": f"{artist_name} Official MV — Demo",
                "published_at": today,
                "channel_title": f"{artist_name} Official",
                "thumbnail": "",
                "views": 48_500_000,
                "likes": 2_450_000,
                "comments": 185_000,
                "url": "",
            },
            {
                "video_id": "demo2",
                "title": f"{artist_name} Comeback Teaser — Demo",
                "published_at": today,
                "channel_title": f"{artist_name} Official",
                "thumbnail": "",
                "views": 11_300_000,
                "likes": 820_000,
                "comments": 74_000,
                "url": "",
            },
        ],
        "global_news": [
            {
                "title": f"{artist_name} draws global attention with a new comeback",
                "description": "Demo global news data.",
                "source": "Demo Global News",
                "published_at": today,
                "url": "",
                "channel": "Global",
            }
        ],
        "naver_news": [
            {
                "title": f"{artist_name}, 컴백 기대감 높이는 새로운 콘텐츠 공개",
                "description": "국내 데모 뉴스입니다.",
                "source": "네이버 뉴스 데모",
                "published_at": today,
                "url": "",
                "channel": "Korea",
            }
        ],
    }


# =========================================================
# 10. COMEBACK SCORE
# =========================================================

def calculate_comeback_score(
    apple_data: dict[str, Any],
    youtube_data: list[dict[str, Any]],
    global_news: list[dict[str, Any]],
    naver_news: list[dict[str, Any]],
) -> tuple[float, dict[str, float]]:
    release_score = freshness_score(
        apple_data.get("latest_album", {}).get("release_date")
    )

    catalog_tracks = apple_data.get("artist", {}).get("catalog_tracks", 0)
    catalog_score = min(float(catalog_tracks) / 50 * 100, 100)

    top_video_views = max(
        (video.get("views", 0) for video in youtube_data),
        default=0,
    )
    youtube_score = normalize_youtube_views(top_video_views)

    recent_global = sum(
        1
        for article in global_news
        if (age := days_since(article.get("published_at"))) is not None and age <= 30
    )
    recent_korean = sum(
        1
        for article in naver_news
        if (age := days_since(article.get("published_at"))) is not None and age <= 30
    )

    global_news_score = min(recent_global / 10 * 100, 100)
    korean_news_score = min(recent_korean / 10 * 100, 100)

    components = {
        "발매 최신성": round(release_score, 1),
        "YouTube 반응": round(youtube_score, 1),
        "글로벌 뉴스": round(global_news_score, 1),
        "국내 뉴스": round(korean_news_score, 1),
        "Apple 카탈로그": round(catalog_score, 1),
    }

    total = (
        components["발매 최신성"] * 0.30
        + components["YouTube 반응"] * 0.35
        + components["글로벌 뉴스"] * 0.15
        + components["국내 뉴스"] * 0.15
        + components["Apple 카탈로그"] * 0.05
    )

    return round(total, 1), components


# =========================================================
# 11. SOLAR AI
# =========================================================

def build_ai_context(
    artist_name: str,
    apple_data: dict[str, Any],
    youtube_data: list[dict[str, Any]],
    global_news: list[dict[str, Any]],
    naver_news: list[dict[str, Any]],
    score: float,
    components: dict[str, float],
) -> str:
    artist = apple_data.get("artist", {})
    album = apple_data.get("latest_album", {})
    tracks = apple_data.get("tracks", [])

    track_text = "\n".join(
        f"- {track.get('name')} / album {track.get('album')} / "
        f"release {format_date(track.get('release_date'))}"
        for track in tracks[:6]
    ) or "- 데이터 없음"

    youtube_text = "\n".join(
        f"- {video.get('title')} / views {video.get('views', 0):,} / "
        f"published {format_date(video.get('published_at'))}"
        for video in youtube_data[:5]
    ) or "- 데이터 없음"

    global_text = "\n".join(
        f"- {article.get('title')} / {article.get('source')} / "
        f"{format_date(article.get('published_at'))}"
        for article in global_news[:6]
    ) or "- 데이터 없음"

    korean_text = "\n".join(
        f"- {article.get('title')} / {article.get('source')} / "
        f"{format_date(article.get('published_at'))}"
        for article in naver_news[:6]
    ) or "- 데이터 없음"

    return f"""
분석 대상: {artist_name}

[Apple iTunes Search]
아티스트: {artist.get('name')}
장르: {artist.get('genre')}
검색된 앨범 수: {artist.get('catalog_albums')}
검색된 트랙 수: {artist.get('catalog_tracks')}
최신 앨범: {album.get('name')}
발매일: {album.get('release_date')}
트랙 수: {album.get('total_tracks')}

검색 트랙:
{track_text}

[YouTube]
{youtube_text}

[글로벌 뉴스]
{global_text}

[국내 뉴스]
{korean_text}

[Comeback Score]
총점: {score}/100
세부 점수: {components}

주의:
- Apple 검색 결과 순서는 공식 인기 순위가 아니라 검색 관련도 순서다.
- 위 데이터에 없는 사실은 만들어내지 않는다.
- 기사 제목만으로 기사 전문을 읽은 것처럼 단정하지 않는다.
- 상관관계와 인과관계를 구분한다.
- 불확실한 해석은 가능성 또는 추정이라고 표시한다.
""".strip()


def ask_solar(
    api_key: str,
    model: str,
    question: str,
    data_context: str,
    chat_history: list[dict[str, str]],
) -> str:
    recent_history = [
        {"role": message["role"], "content": message["content"]}
        for message in chat_history[-6:]
        if message.get("role") in {"user", "assistant"}
    ]

    system_prompt = f"""
당신은 K-POP 데이터와 마케팅을 분석하는 AI 애널리스트입니다.

답변 원칙:
1. 한국어로 답합니다.
2. 핵심 결론을 먼저 제시합니다.
3. 제공된 데이터에 근거해 숫자를 구체적으로 활용합니다.
4. 사실과 해석을 구분합니다.
5. 국내 반응과 해외 반응을 필요할 때 비교합니다.
6. 불확실한 내용은 추정이라고 표시합니다.
7. Apple 검색 결과를 인기 순위라고 표현하지 않습니다.

현재 분석 데이터:
{data_context}
""".strip()

    messages = [{"role": "system", "content": system_prompt}]
    messages.extend(recent_history)
    messages.append({"role": "user", "content": question})

    result = safe_request(
        "POST",
        SOLAR_CHAT_API_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json_body={
            "model": model,
            "messages": messages,
            "temperature": 0.3,
            "max_tokens": 900,
        },
        timeout=50,
    )

    try:
        return result["choices"][0]["message"]["content"].strip()
    except (KeyError, IndexError, TypeError, AttributeError) as exc:
        raise RuntimeError(f"Solar 응답 형식을 읽지 못했습니다: {result}") from exc


def generate_fallback_answer(
    artist_name: str,
    question: str,
    score: float,
    components: dict[str, float],
    apple_data: dict[str, Any],
    youtube_data: list[dict[str, Any]],
    global_news: list[dict[str, Any]],
    naver_news: list[dict[str, Any]],
) -> str:
    album = apple_data.get("latest_album", {})
    strongest = max(components, key=components.get)
    weakest = min(components, key=components.get)
    top_video = max(youtube_data, key=lambda x: x.get("views", 0), default={})

    return f"""
**{artist_name}의 현재 Comeback Score는 {score}/100점**입니다.

가장 강한 신호는 **{strongest} {components[strongest]}점**, 상대적으로 약한 신호는
**{weakest} {components[weakest]}점**입니다.

- Apple 최신 확인 앨범: **{album.get("name", "정보 없음")}**
- 발매일: **{format_date(album.get("release_date"))}**
- 최근 영상 중 최고 조회수: **{format_number(top_video.get("views", 0))}**
- 글로벌 뉴스: **{len(global_news)}건**
- 국내 뉴스: **{len(naver_news)}건**

“{question}”에 대한 초기 해석은 **{strongest}가 현재 관심도를 주도하지만,
{weakest}가 보완되는지 추가 관찰해야 한다**는 것입니다.

※ Solar API가 연결되지 않아 규칙 기반으로 답변했습니다.
""".strip()


# =========================================================
# 12. RENDERING
# =========================================================

def render_album_card(artist_name: str, apple_data: dict[str, Any]) -> None:
    album = apple_data.get("latest_album", {})
    image_url = album.get("image", "")
    apple_url = album.get("apple_url", "")

    image_html = (
        f'<img class="album-cover" src="{escape_text(image_url)}" '
        f'alt="{escape_text(album.get("name"))}">'
        if image_url
        else (
            '<div class="album-cover" style="display:flex;align-items:center;'
            'justify-content:center;font-size:2.1rem;">🍎</div>'
        )
    )

    link_html = (
        f'<div style="margin-top:10px;"><a href="{escape_text(apple_url)}" '
        'target="_blank" style="color:#6957d9;text-decoration:none;'
        'font-weight:800;">Apple Music에서 열기 ↗</a></div>'
        if apple_url
        else ""
    )

    st.markdown(
        f"""
        <div class="album-card">
            {image_html}
            <div>
                <div class="muted">{escape_text(artist_name)} · Apple Latest Release</div>
                <div class="album-name">{escape_text(album.get("name", "앨범 정보 없음"))}</div>
                <div class="muted">
                    발매일 {escape_text(format_date(album.get("release_date")))}<br>
                    {escape_text(album.get("album_type", "Album"))} ·
                    {escape_text(album.get("total_tracks", 0))} tracks
                </div>
                {link_html}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_track_list(tracks: list[dict[str, Any]]) -> None:
    if not tracks:
        st.info("Apple 카탈로그에서 표시할 트랙을 찾지 못했습니다.")
        return

    for index, track in enumerate(tracks[:8], start=1):
        with st.container(border=True):
            col1, col2 = st.columns([4, 1])

            with col1:
                apple_url = track.get("apple_url", "")
                title = track.get("name", "제목 없음")
                st.markdown(
                    f"**{index}. [{title}]({apple_url})**"
                    if apple_url
                    else f"**{index}. {title}**"
                )
                st.caption(
                    f"{track.get('album', '')} · "
                    f"{format_date(track.get('release_date'))}"
                )

            with col2:
                preview_url = track.get("preview_url", "")
                if preview_url:
                    st.audio(preview_url, format="audio/mpeg")


def render_news_cards(news_items: list[dict[str, Any]]) -> None:
    if not news_items:
        st.info("표시할 뉴스가 없습니다.")
        return

    for article in news_items[:8]:
        title = escape_text(article.get("title", "제목 없음"))
        source = escape_text(article.get("source", "출처 미상"))
        date_text = escape_text(format_date(article.get("published_at")))
        url = article.get("url", "")

        title_html = (
            f'<a class="news-title" href="{escape_text(url)}" '
            f'target="_blank">{title}</a>'
            if url
            else f'<div class="news-title">{title}</div>'
        )

        st.markdown(
            f"""
            <div class="news-card">
                {title_html}
                <div class="news-meta">{source} · {date_text}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_youtube_videos(videos: list[dict[str, Any]]) -> None:
    if not videos:
        st.info("표시할 YouTube 영상이 없습니다.")
        return

    for video in videos[:4]:
        with st.container(border=True):
            left, right = st.columns([1.1, 2.3])

            with left:
                if video.get("thumbnail"):
                    st.image(video["thumbnail"], use_container_width=True)
                else:
                    st.markdown("### 🎬")

            with right:
                title = video.get("title", "제목 없음")
                url = video.get("url", "")
                st.markdown(f"**[{title}]({url})**" if url else f"**{title}**")
                st.caption(
                    f"{video.get('channel_title', '')} · "
                    f"{format_date(video.get('published_at'))}"
                )

                metrics = st.columns(3)
                metrics[0].metric("조회수", format_number(video.get("views", 0)))
                metrics[1].metric("좋아요", format_number(video.get("likes", 0)))
                metrics[2].metric("댓글", format_number(video.get("comments", 0)))


# =========================================================
# 13. SECRETS / SIDEBAR
# =========================================================

youtube_api_key = get_secret("YOUTUBE_API_KEY")
mediastack_api_key = get_secret("MEDIASTACK_API_KEY")
naver_client_id = get_secret("NAVER_CLIENT_ID")
naver_client_secret = get_secret("NAVER_CLIENT_SECRET")
solar_api_key = get_secret("SOLAR_API_KEY")
solar_model = get_secret("SOLAR_MODEL", "solar-pro3")

youtube_connected = bool(youtube_api_key)
mediastack_connected = bool(mediastack_api_key)
naver_connected = bool(naver_client_id and naver_client_secret)
solar_connected = bool(solar_api_key)

with st.sidebar:
    st.markdown("## 📡 Radar Control")

    selected_artist = st.selectbox(
        "분석할 아티스트",
        list(ARTISTS.keys()),
        index=0,
    )

    st.markdown("---")
    st.markdown("### 데이터 연결 상태")
    st.write("🟢 Apple Music Catalog")
    st.write(f"{'🟢' if youtube_connected else '⚪'} YouTube")
    st.write(f"{'🟢' if mediastack_connected else '⚪'} Mediastack")
    st.write(f"{'🟢' if naver_connected else '⚪'} 네이버 뉴스")
    st.write(f"{'🟢' if solar_connected else '⚪'} Solar AI")

    st.caption(
        "Apple 검색 API는 별도 키 없이 작동합니다. "
        "연결되지 않은 다른 API는 데모 데이터 또는 규칙 기반 답변으로 대체됩니다."
    )

    st.markdown("---")

    if st.button("🔄 데이터 새로고침", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

    demo_mode = st.toggle(
        "데모 모드 강제 사용",
        value=False,
        help="API 키가 있어도 샘플 데이터로 화면을 확인합니다.",
    )


# =========================================================
# 14. LOAD DATA
# =========================================================

config = ARTISTS[selected_artist]
demo = get_demo_bundle(selected_artist)

apple_data = demo["apple"]
youtube_data = demo["youtube"]
global_news = demo["global_news"]
naver_news = demo["naver_news"]

active_sources: list[str] = []
api_errors: list[str] = []
demo_sources: list[str] = []

if demo_mode:
    active_sources = [
        "Apple Demo",
        "YouTube Demo",
        "Global News Demo",
        "Korean News Demo",
    ]
    demo_sources = ["Apple", "YouTube", "Mediastack", "네이버 뉴스"]
else:
    try:
        apple_data = get_apple_music_data(config["apple_query"])
        active_sources.append("Apple Live")
    except RuntimeError as error:
        api_errors.append(f"Apple: {error}")
        active_sources.append("Apple Demo")
        demo_sources.append("Apple")

    if youtube_connected:
        try:
            youtube_data = get_youtube_data(
                config["youtube_query"],
                youtube_api_key,
            )
            active_sources.append("YouTube Live")
        except RuntimeError as error:
            api_errors.append(f"YouTube: {error}")
            active_sources.append("YouTube Demo")
            demo_sources.append("YouTube")
    else:
        active_sources.append("YouTube Demo")
        demo_sources.append("YouTube")

    if mediastack_connected:
        try:
            global_news = get_global_news(
                config["global_news_query"],
                mediastack_api_key,
            )
            active_sources.append("Mediastack Live")
        except RuntimeError as error:
            api_errors.append(f"Mediastack: {error}")
            active_sources.append("Global News Demo")
            demo_sources.append("Mediastack")
    else:
        active_sources.append("Global News Demo")
        demo_sources.append("Mediastack")

    if naver_connected:
        try:
            naver_news = get_naver_news(
                config["naver_news_query"],
                naver_client_id,
                naver_client_secret,
            )
            active_sources.append("Naver News Live")
        except RuntimeError as error:
            api_errors.append(f"Naver: {error}")
            active_sources.append("Korean News Demo")
            demo_sources.append("네이버 뉴스")
    else:
        active_sources.append("Korean News Demo")
        demo_sources.append("네이버 뉴스")

score, components = calculate_comeback_score(
    apple_data,
    youtube_data,
    global_news,
    naver_news,
)


# =========================================================
# 15. HEADER / SUMMARY
# =========================================================

badges = "".join(
    f'<span class="badge">{escape_text(source)}</span>'
    for source in active_sources
)

st.markdown(
    f"""
    <div class="hero">
        <div class="eyebrow">K-POP DATA & AI INTELLIGENCE</div>
        <h1 class="hero-title">K-POP Comeback Radar</h1>
        <div class="hero-subtitle">
            {escape_text(config["emoji"])}
            <strong>{escape_text(selected_artist)}</strong>의
            Apple 음악 카탈로그·YouTube·글로벌 뉴스·국내 뉴스 신호를 추적하고,
            Solar AI 애널리스트에게 데이터 기반 질문을 해보세요.
        </div>
        <div style="margin-top:16px;">{badges}</div>
    </div>
    """,
    unsafe_allow_html=True,
)

if api_errors:
    with st.expander(f"⚠️ 일부 API 연결 오류 {len(api_errors)}건"):
        for error in api_errors:
            st.warning(error)

if demo_mode:
    st.info("현재 전체 영역이 데모 모드로 실행 중입니다.")
elif demo_sources:
    st.info("현재 데모 데이터가 사용되는 영역: " + ", ".join(demo_sources))
else:
    st.success("모든 데이터 영역이 실시간 API로 연결되었습니다.")

artist_data = apple_data.get("artist", {})
album_data = apple_data.get("latest_album", {})
top_video = max(youtube_data, key=lambda x: x.get("views", 0), default={})

metric_columns = st.columns(5)
metric_columns[0].metric(
    "Apple Catalog Albums",
    f"{artist_data.get('catalog_albums', 0)}개",
)
metric_columns[1].metric(
    "Apple Catalog Tracks",
    f"{artist_data.get('catalog_tracks', 0)}개",
)
metric_columns[2].metric(
    "Top YouTube Views",
    format_number(top_video.get("views", 0)),
)
metric_columns[3].metric("Global News", f"{len(global_news)}건")
metric_columns[4].metric("Korean News", f"{len(naver_news)}건")


# =========================================================
# 16. MAIN DASHBOARD
# =========================================================

left, center, right = st.columns([1.25, 1.6, 1.0], gap="large")

with left:
    st.markdown(
        '<div class="section-title">🍎 Latest Apple Release</div>',
        unsafe_allow_html=True,
    )
    render_album_card(selected_artist, apple_data)

    st.markdown(
        '<div class="section-title">🎧 Apple Search Tracks</div>',
        unsafe_allow_html=True,
    )
    st.caption("Apple 검색 관련도 순서이며 공식 인기 순위는 아닙니다.")
    render_track_list(apple_data.get("tracks", []))

with center:
    st.markdown(
        '<div class="section-title">🎬 YouTube Signal</div>',
        unsafe_allow_html=True,
    )
    render_youtube_videos(youtube_data)

with right:
    st.markdown(
        '<div class="section-title">📈 Comeback Score</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="score-card">
            <div class="muted">현재 레이더 점수</div>
            <div class="score-number">{score:.0f}</div>
            <div style="font-size:1.05rem;font-weight:900;margin-top:9px;color:#3a315f;">
                {escape_text(score_label(score))}
            </div>
            <div class="muted" style="margin-top:10px;">
                발매 최신성·YouTube·국내외 뉴스·Apple 카탈로그를
                합산한 학습용 자체 지표입니다.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    radar_df = pd.DataFrame(
        {"지표": list(components.keys()), "점수": list(components.values())}
    )

    radar_fig = px.line_polar(
        radar_df,
        r="점수",
        theta="지표",
        line_close=True,
        range_r=[0, 100],
    )
    radar_fig.update_traces(fill="toself", line=dict(color="#6957d9"))
    radar_fig.update_layout(
        height=385,
        margin=dict(l=18, r=18, t=40, b=30),
        paper_bgcolor="rgba(0,0,0,0)",
        polar=dict(
            bgcolor="rgba(255,255,255,.55)",
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                gridcolor="rgba(105,87,217,.14)",
                tickfont=dict(color="#77738b"),
            ),
            angularaxis=dict(
                gridcolor="rgba(105,87,217,.14)",
                tickfont=dict(color="#373052", size=11),
            ),
        ),
        showlegend=False,
        font=dict(color="#373052"),
    )
    st.plotly_chart(
        radar_fig,
        use_container_width=True,
        config={"displayModeBar": False},
    )


# =========================================================
# 17. RELEASE HISTORY
# =========================================================

st.markdown("---")
st.markdown(
    '<div class="section-title">💿 Recent Apple Catalog Releases</div>',
    unsafe_allow_html=True,
)

albums_df = pd.DataFrame(apple_data.get("albums", []))

if albums_df.empty:
    st.info("표시할 앨범 이력이 없습니다.")
else:
    albums_df["발매일"] = albums_df["release_date"].map(format_date)
    albums_df = albums_df.rename(
        columns={
            "name": "앨범",
            "track_count": "트랙 수",
        }
    )
    st.dataframe(
        albums_df[["앨범", "발매일", "트랙 수"]],
        use_container_width=True,
        hide_index=True,
    )


# =========================================================
# 18. NEWS
# =========================================================

st.markdown("---")
st.markdown(
    '<div class="section-title">📰 Comeback News Monitor</div>',
    unsafe_allow_html=True,
)

global_tab, korean_tab = st.tabs(["🌎 Global News", "🇰🇷 Korean News"])

with global_tab:
    st.caption("Mediastack을 통해 수집한 영문권 기사입니다.")
    render_news_cards(global_news)

with korean_tab:
    st.caption("네이버 검색 API를 통해 수집한 국내 최신 기사입니다.")
    render_news_cards(naver_news)


# =========================================================
# 19. INTERPRETATION
# =========================================================

st.markdown("---")
st.markdown(
    '<div class="section-title">🔍 Radar Interpretation</div>',
    unsafe_allow_html=True,
)

strongest = max(components, key=components.get)
weakest = min(components, key=components.get)
release_age = days_since(album_data.get("release_date"))

if release_age is None:
    release_description = "발매일을 확인할 수 없습니다."
elif release_age == 0:
    release_description = "오늘 공개된 발매작이 감지되었습니다."
else:
    release_description = f"최근 발매작은 약 {release_age}일 전 공개됐습니다."

interpretation_columns = st.columns(3)

with interpretation_columns[0]:
    st.markdown(
        f"""
        <div class="glass-card">
            <div class="muted">STRONGEST SIGNAL</div>
            <h3 style="color:#443b70;">{escape_text(strongest)}</h3>
            <div class="muted">
                {components[strongest]:.1f}점으로 현재 분석 지표 중 가장 높습니다.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with interpretation_columns[1]:
    st.markdown(
        f"""
        <div class="glass-card">
            <div class="muted">NEEDS MONITORING</div>
            <h3 style="color:#443b70;">{escape_text(weakest)}</h3>
            <div class="muted">
                {components[weakest]:.1f}점입니다. 데이터 누적에 따라 달라질 수 있습니다.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with interpretation_columns[2]:
    st.markdown(
        f"""
        <div class="glass-card">
            <div class="muted">RELEASE TIMING</div>
            <h3 style="color:#443b70;">Latest Signal</h3>
            <div class="muted">{escape_text(release_description)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# =========================================================
# 20. SOLAR CHAT
# =========================================================

st.markdown("---")
st.markdown(
    '<div class="section-title">🤖 Ask the Solar K-POP Analyst</div>',
    unsafe_allow_html=True,
)

st.caption(
    "예: 국내와 해외 반응의 차이를 분석해줘 · "
    "이번 컴백에서 가장 강한 신호는 무엇이야? · "
    "마케팅 관점의 시사점을 정리해줘"
)

if "chat_artist" not in st.session_state:
    st.session_state.chat_artist = selected_artist

if st.session_state.chat_artist != selected_artist:
    st.session_state.chat_artist = selected_artist
    st.session_state.chat_messages = []

if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = [
        {
            "role": "assistant",
            "content": (
                f"{selected_artist}의 국내외 컴백 데이터를 분석하고 있어요. "
                "궁금한 내용을 질문해주세요."
            ),
        }
    ]

for message in st.session_state.chat_messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

question = st.chat_input(f"{selected_artist}에 대해 질문해보세요")

if question:
    st.session_state.chat_messages.append(
        {"role": "user", "content": question}
    )

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Solar가 데이터를 분석하고 있습니다..."):
            if solar_connected and not demo_mode:
                context = build_ai_context(
                    selected_artist,
                    apple_data,
                    youtube_data,
                    global_news,
                    naver_news,
                    score,
                    components,
                )

                try:
                    answer = ask_solar(
                        api_key=solar_api_key,
                        model=solar_model,
                        question=question,
                        data_context=context,
                        chat_history=st.session_state.chat_messages,
                    )
                except RuntimeError as error:
                    answer = (
                        f"Solar API 연결 중 오류가 발생했습니다.\n\n"
                        f"`{error}`\n\n"
                        + generate_fallback_answer(
                            selected_artist,
                            question,
                            score,
                            components,
                            apple_data,
                            youtube_data,
                            global_news,
                            naver_news,
                        )
                    )
            else:
                answer = generate_fallback_answer(
                    selected_artist,
                    question,
                    score,
                    components,
                    apple_data,
                    youtube_data,
                    global_news,
                    naver_news,
                )

        st.markdown(answer)

    st.session_state.chat_messages.append(
        {"role": "assistant", "content": answer}
    )


# =========================================================
# 21. FOOTER
# =========================================================

st.markdown("---")
st.caption(
    "K-POP Comeback Radar MVP · "
    "Apple iTunes Search API · YouTube Data API · Mediastack · "
    "Naver Search API · Upstage Solar · "
    "Apple 검색 결과는 공식 인기 순위가 아니며 Comeback Score는 비공식 학습용 지표입니다. · "
"APPLE-ONLY BUILD 2026-07-23"
)
