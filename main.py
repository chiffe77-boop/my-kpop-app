from __future__ import annotations

import base64
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

SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_API_URL = "https://api.spotify.com/v1"
YOUTUBE_API_URL = "https://www.googleapis.com/youtube/v3"
NEWS_API_URL = "https://newsapi.org/v2/everything"
NAVER_NEWS_API_URL = "https://openapi.naver.com/v1/search/news.json"
SOLAR_CHAT_API_URL = "https://api.upstage.ai/v1/solar/chat/completions"

ARTISTS: dict[str, dict[str, str]] = {
    "aespa": {
        "spotify_query": "aespa",
        "youtube_query": "aespa official",
        "global_news_query": 'aespa',
        "naver_news_query": "에스파",
        "emoji": "🪩",
    },
    "BLACKPINK": {
        "spotify_query": "BLACKPINK",
        "youtube_query": "BLACKPINK official",
        "global_news_query": '"BLACKPINK"',
        "naver_news_query": "블랙핑크",
        "emoji": "🖤",
    },
    "BTS": {
        "spotify_query": "BTS",
        "youtube_query": "BTS official BANGTANTV",
        "global_news_query": '"BTS" AND K-pop',
        "naver_news_query": "방탄소년단",
        "emoji": "💜",
    },
    "IVE": {
        "spotify_query": "IVE",
        "youtube_query": "IVE official",
        "global_news_query": '"IVE" AND K-pop',
        "naver_news_query": "아이브",
        "emoji": "✨",
    },
    "LE SSERAFIM": {
        "spotify_query": "LE SSERAFIM",
        "youtube_query": "LE SSERAFIM official",
        "global_news_query": '"LE SSERAFIM"',
        "naver_news_query": "르세라핌",
        "emoji": "🔥",
    },
    "NCT DREAM": {
        "spotify_query": "NCT DREAM",
        "youtube_query": "NCT DREAM official",
        "global_news_query": '"NCT DREAM"',
        "naver_news_query": "엔시티 드림",
        "emoji": "💚",
    },
    "NewJeans": {
        "spotify_query": "NewJeans",
        "youtube_query": "NewJeans official",
        "global_news_query": '"NewJeans"',
        "naver_news_query": "뉴진스",
        "emoji": "🐰",
    },
    "RIIZE": {
        "spotify_query": "RIIZE",
        "youtube_query": "RIIZE official",
        "global_news_query": '"RIIZE" AND K-pop',
        "naver_news_query": "라이즈",
        "emoji": "🌅",
    },
    "SEVENTEEN": {
        "spotify_query": "SEVENTEEN",
        "youtube_query": "SEVENTEEN official",
        "global_news_query": '"SEVENTEEN" AND K-pop',
        "naver_news_query": "세븐틴",
        "emoji": "💎",
    },
    "Stray Kids": {
        "spotify_query": "Stray Kids",
        "youtube_query": "Stray Kids official",
        "global_news_query": '"Stray Kids"',
        "naver_news_query": "스트레이 키즈",
        "emoji": "⚡",
    },
}


# =========================================================
# 3. CSS
# =========================================================

st.markdown(
    """
    <style>
        .stApp {
            background:
                radial-gradient(circle at 15% 8%, rgba(139,92,246,.18), transparent 25%),
                radial-gradient(circle at 85% 8%, rgba(236,72,153,.15), transparent 24%),
                linear-gradient(180deg, #080a14 0%, #101427 100%);
            color: #f7f7fb;
        }

        [data-testid="stSidebar"] {
            background: rgba(11,13,26,.97);
            border-right: 1px solid rgba(255,255,255,.08);
        }

        .block-container {
            max-width: 1400px;
            padding-top: 1.8rem;
            padding-bottom: 3rem;
        }

        .hero {
            padding: 28px 30px;
            border: 1px solid rgba(255,255,255,.10);
            border-radius: 24px;
            background:
                linear-gradient(135deg, rgba(139,92,246,.20), rgba(236,72,153,.10)),
                rgba(15,18,35,.84);
            box-shadow: 0 18px 50px rgba(0,0,0,.28);
            margin-bottom: 22px;
        }

        .eyebrow {
            color: #c4b5fd;
            font-size: .78rem;
            font-weight: 800;
            letter-spacing: .18em;
            text-transform: uppercase;
            margin-bottom: 8px;
        }

        .hero-title {
            font-size: clamp(2rem, 4vw, 4rem);
            line-height: 1.02;
            font-weight: 900;
            margin: 0;
            background: linear-gradient(90deg, #fff, #d8b4fe, #f9a8d4);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .hero-subtitle {
            color: #b8bfd4;
            margin-top: 13px;
            font-size: 1rem;
            max-width: 850px;
            line-height: 1.65;
        }

        .section-title {
            font-size: 1.32rem;
            font-weight: 850;
            margin: 14px 0;
        }

        .glass-card {
            height: 100%;
            padding: 20px;
            border-radius: 20px;
            background: rgba(21,25,48,.86);
            border: 1px solid rgba(255,255,255,.09);
            box-shadow: 0 12px 35px rgba(0,0,0,.22);
        }

        .album-card {
            display: flex;
            gap: 18px;
            align-items: center;
            padding: 18px;
            border-radius: 20px;
            background: rgba(21,25,48,.90);
            border: 1px solid rgba(255,255,255,.09);
            margin-bottom: 14px;
        }

        .album-cover {
            width: 116px;
            height: 116px;
            min-width: 116px;
            border-radius: 16px;
            object-fit: cover;
            background: #282d4d;
        }

        .album-name {
            font-size: 1.12rem;
            font-weight: 850;
            margin: 7px 0;
        }

        .muted {
            color: #aeb5cb;
            font-size: .9rem;
            line-height: 1.55;
        }

        .score-card {
            text-align: center;
            padding: 26px 18px;
            border-radius: 22px;
            background:
                radial-gradient(circle at 50% 5%, rgba(236,72,153,.23), transparent 42%),
                rgba(21,25,48,.90);
            border: 1px solid rgba(255,255,255,.10);
        }

        .score-number {
            font-size: 3.8rem;
            line-height: 1;
            font-weight: 950;
            background: linear-gradient(90deg, #c4b5fd, #f9a8d4);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .news-card {
            padding: 16px 17px;
            margin-bottom: 11px;
            border-radius: 17px;
            background: rgba(21,25,48,.84);
            border: 1px solid rgba(255,255,255,.08);
        }

        .news-title {
            color: #fff;
            font-weight: 800;
            font-size: .98rem;
            line-height: 1.45;
            text-decoration: none;
        }

        .news-title:hover { color: #d8b4fe; }

        .news-meta {
            color: #959db9;
            font-size: .78rem;
            margin-top: 8px;
        }

        .badge {
            display: inline-block;
            padding: 4px 9px;
            border-radius: 999px;
            font-size: .72rem;
            font-weight: 750;
            margin: 2px 3px 2px 0;
            background: rgba(139,92,246,.16);
            border: 1px solid rgba(196,181,253,.22);
            color: #ddd6fe;
        }

        div[data-testid="stMetric"] {
            background: rgba(21,25,48,.84);
            border: 1px solid rgba(255,255,255,.08);
            padding: 16px;
            border-radius: 18px;
        }

        div[data-testid="stChatMessage"] {
            background: rgba(21,25,48,.70);
            border: 1px solid rgba(255,255,255,.07);
            border-radius: 17px;
            padding: 9px 13px;
        }

        .stButton > button {
            border-radius: 12px;
            border: 1px solid rgba(255,255,255,.10);
            font-weight: 750;
        }

        @media (max-width: 700px) {
            .block-container {
                padding: 1rem;
            }

            .hero {
                padding: 21px 19px;
                border-radius: 19px;
            }

            .hero-title { font-size: 2.15rem; }
            .hero-subtitle { font-size: .91rem; }

            .album-card {
                align-items: flex-start;
                gap: 12px;
                padding: 14px;
            }

            .album-cover {
                width: 86px;
                height: 86px;
                min-width: 86px;
            }

            .score-number { font-size: 3rem; }
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# 4. GENERIC HELPERS
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
    data: dict[str, Any] | None = None,
    json_body: dict[str, Any] | None = None,
    timeout: int = 20,
) -> dict[str, Any]:
    try:
        response = requests.request(
            method=method,
            url=url,
            headers=headers,
            params=params,
            data=data,
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
    clean = re.sub(r"<[^>]+>", "", value)
    return html.unescape(clean).strip()


def parse_datetime(value: str | None) -> datetime | None:
    if not value:
        return None

    formats = (
        None,
        "%a, %d %b %Y %H:%M:%S %z",
        "%Y-%m-%d",
    )

    for date_format in formats:
        try:
            if date_format is None:
                parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
            else:
                parsed = datetime.strptime(value, date_format)

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


def normalize_popularity(value: int | float | None) -> float:
    try:
        return max(0.0, min(float(value or 0), 100.0))
    except (TypeError, ValueError):
        return 0.0


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


# =========================================================
# 5. SPOTIFY
# =========================================================

@st.cache_data(ttl=300, show_spinner=False)
def get_spotify_token(client_id: str, client_secret: str) -> str:
    encoded = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()

    result = safe_request(
        "POST",
        SPOTIFY_TOKEN_URL,
        headers={
            "Authorization": f"Basic {encoded}",
            "Content-Type": "application/x-www-form-urlencoded",
        },
        data={"grant_type": "client_credentials"},
    )

    token = result.get("access_token")
    if not token:
        raise RuntimeError("Spotify access token을 받지 못했습니다.")
    return token


@st.cache_data(ttl=1800, show_spinner=False)
def get_spotify_data(
    artist_query: str,
    client_id: str,
    client_secret: str,
) -> dict[str, Any]:
    token = get_spotify_token(client_id, client_secret)
    headers = {"Authorization": f"Bearer {token}"}

    search_result = safe_request(
        "GET",
        f"{SPOTIFY_API_URL}/search",
        headers=headers,
        params={"q": artist_query, "type": "artist", "limit": 5},
    )

    candidates = search_result.get("artists", {}).get("items", [])
    if not candidates:
        raise RuntimeError("Spotify에서 아티스트를 찾지 못했습니다.")

    artist = next(
        (
            item for item in candidates
            if item.get("name", "").casefold() == artist_query.casefold()
        ),
        candidates[0],
    )

    artist_id = artist["id"]

    tracks_result = safe_request(
        "GET",
        f"{SPOTIFY_API_URL}/artists/{artist_id}/top-tracks",
        headers=headers,
        params={"market": "KR"},
    )

    albums_result = safe_request(
        "GET",
        f"{SPOTIFY_API_URL}/artists/{artist_id}/albums",
        headers=headers,
        params={
            "include_groups": "album,single",
            "market": "KR",
            "limit": 30,
        },
    )

    albums = albums_result.get("items", [])
    unique_albums: list[dict[str, Any]] = []
    seen: set[str] = set()

    for album in albums:
        key = album.get("name", "").strip().casefold()
        if key and key not in seen:
            seen.add(key)
            unique_albums.append(album)

    unique_albums.sort(key=lambda x: x.get("release_date", ""), reverse=True)
    latest = unique_albums[0] if unique_albums else {}

    artist_images = artist.get("images", [])
    album_images = latest.get("images", [])

    return {
        "artist": {
            "name": artist.get("name", artist_query),
            "followers": artist.get("followers", {}).get("total", 0),
            "popularity": artist.get("popularity", 0),
            "genres": artist.get("genres", []),
            "image": artist_images[0]["url"] if artist_images else "",
            "spotify_url": artist.get("external_urls", {}).get("spotify", ""),
        },
        "latest_album": {
            "name": latest.get("name", "앨범 정보 없음"),
            "release_date": latest.get("release_date", ""),
            "album_type": latest.get("album_type", ""),
            "total_tracks": latest.get("total_tracks", 0),
            "image": album_images[0]["url"] if album_images else "",
            "spotify_url": latest.get("external_urls", {}).get("spotify", ""),
        },
        "top_tracks": [
            {
                "name": track.get("name", ""),
                "popularity": track.get("popularity", 0),
                "album": track.get("album", {}).get("name", ""),
                "spotify_url": track.get("external_urls", {}).get("spotify", ""),
            }
            for track in tracks_result.get("tracks", [])[:10]
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
# 7. NEWSAPI: GLOBAL NEWS
# =========================================================

@st.cache_data(ttl=1800, show_spinner=False)
def get_global_news(query: str, api_key: str) -> list[dict[str, Any]]:
    result = safe_request(
        "GET",
        NEWS_API_URL,
        headers={"X-Api-Key": api_key},
        params={
            "q": query,
            "language": "en",
            "sortBy": "publishedAt",
            "pageSize": 10,
        },
    )

    return [
        {
            "title": article.get("title", ""),
            "description": article.get("description", ""),
            "source": article.get("source", {}).get("name", ""),
            "published_at": article.get("publishedAt", ""),
            "url": article.get("url", ""),
            "image": article.get("urlToImage", ""),
            "channel": "Global",
        }
        for article in result.get("articles", [])
        if article.get("title") and article.get("url")
    ]


# =========================================================
# 8. NAVER SEARCH API: KOREAN NEWS
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

    news: list[dict[str, Any]] = []

    for item in result.get("items", []):
        news.append(
            {
                "title": strip_html_tags(item.get("title")),
                "description": strip_html_tags(item.get("description")),
                "source": "네이버 뉴스",
                "published_at": item.get("pubDate", ""),
                "url": item.get("originallink") or item.get("link", ""),
                "naver_url": item.get("link", ""),
                "image": "",
                "channel": "Korea",
            }
        )

    return news


# =========================================================
# 9. DEMO DATA
# =========================================================

def get_demo_bundle(artist_name: str) -> dict[str, Any]:
    today = datetime.now(timezone.utc).isoformat()

    return {
        "spotify": {
            "artist": {
                "name": artist_name,
                "followers": 12_540_000,
                "popularity": 84,
                "genres": ["k-pop", "korean pop"],
                "image": "",
                "spotify_url": "",
            },
            "latest_album": {
                "name": f"{artist_name} Demo Album",
                "release_date": datetime.now().strftime("%Y-%m-%d"),
                "album_type": "album",
                "total_tracks": 8,
                "image": "",
                "spotify_url": "",
            },
            "top_tracks": [
                {"name": "Demo Track A", "popularity": 91, "album": "Demo Album", "spotify_url": ""},
                {"name": "Demo Track B", "popularity": 86, "album": "Demo Album", "spotify_url": ""},
                {"name": "Demo Track C", "popularity": 79, "album": "Demo Album", "spotify_url": ""},
                {"name": "Demo Track D", "popularity": 73, "album": "Demo Album", "spotify_url": ""},
                {"name": "Demo Track E", "popularity": 67, "album": "Demo Album", "spotify_url": ""},
            ],
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
                "image": "",
                "channel": "Global",
            }
        ],
        "naver_news": [
            {
                "title": f"{artist_name}, 컴백 기대감 높이는 새로운 콘텐츠 공개",
                "description": "API 키가 없을 때 표시되는 국내 데모 뉴스입니다.",
                "source": "네이버 뉴스 데모",
                "published_at": today,
                "url": "",
                "naver_url": "",
                "image": "",
                "channel": "Korea",
            }
        ],
    }


# =========================================================
# 10. COMEBACK SCORE
# =========================================================

def calculate_comeback_score(
    spotify_data: dict[str, Any],
    youtube_data: list[dict[str, Any]],
    global_news: list[dict[str, Any]],
    naver_news: list[dict[str, Any]],
) -> tuple[float, dict[str, float]]:
    spotify_score = normalize_popularity(
        spotify_data.get("artist", {}).get("popularity", 0)
    )

    release_score = freshness_score(
        spotify_data.get("latest_album", {}).get("release_date")
    )

    top_video_views = max(
        (video.get("views", 0) for video in youtube_data),
        default=0,
    )
    youtube_score = normalize_youtube_views(top_video_views)

    recent_global = sum(
        1 for article in global_news
        if days_since(article.get("published_at")) is not None
        and days_since(article.get("published_at")) <= 30
    )

    recent_korean = sum(
        1 for article in naver_news
        if days_since(article.get("published_at")) is not None
        and days_since(article.get("published_at")) <= 30
    )

    news_score = min((recent_global + recent_korean) / 20 * 100, 100)

    components = {
        "Spotify 인기도": round(spotify_score, 1),
        "발매 최신성": round(release_score, 1),
        "YouTube 반응": round(youtube_score, 1),
        "뉴스 화제성": round(news_score, 1),
    }

    total = (
        components["Spotify 인기도"] * 0.30
        + components["발매 최신성"] * 0.30
        + components["YouTube 반응"] * 0.25
        + components["뉴스 화제성"] * 0.15
    )

    return round(total, 1), components


# =========================================================
# 11. SOLAR AI
# =========================================================

def build_ai_context(
    artist_name: str,
    spotify_data: dict[str, Any],
    youtube_data: list[dict[str, Any]],
    global_news: list[dict[str, Any]],
    naver_news: list[dict[str, Any]],
    score: float,
    components: dict[str, float],
) -> str:
    artist = spotify_data.get("artist", {})
    album = spotify_data.get("latest_album", {})
    tracks = spotify_data.get("top_tracks", [])

    track_text = "\n".join(
        f"- {x.get('name')} / popularity {x.get('popularity')}"
        for x in tracks[:5]
    ) or "- 데이터 없음"

    youtube_text = "\n".join(
        (
            f"- {x.get('title')} / views {x.get('views', 0):,} / "
            f"published {format_date(x.get('published_at'))}"
        )
        for x in youtube_data[:5]
    ) or "- 데이터 없음"

    global_text = "\n".join(
        (
            f"- {x.get('title')} / {x.get('source')} / "
            f"{format_date(x.get('published_at'))}"
        )
        for x in global_news[:6]
    ) or "- 데이터 없음"

    korean_text = "\n".join(
        (
            f"- {x.get('title')} / {x.get('source')} / "
            f"{format_date(x.get('published_at'))}"
        )
        for x in naver_news[:6]
    ) or "- 데이터 없음"

    return f"""
분석 대상: {artist_name}

[Spotify]
인기도: {artist.get('popularity', 0)}
팔로워: {artist.get('followers', 0):,}
장르: {', '.join(artist.get('genres', []))}
최신 앨범: {album.get('name')}
발매일: {album.get('release_date')}
트랙 수: {album.get('total_tracks')}

인기곡:
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

분석 규칙:
- 위 데이터에 없는 사실은 만들어내지 않는다.
- 기사 제목만으로 기사 전체 내용을 아는 것처럼 단정하지 않는다.
- 상관관계와 인과관계를 구분한다.
- 수치는 수집 시점 기준이라고 설명한다.
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
        {
            "role": message["role"],
            "content": message["content"],
        }
        for message in chat_history[-6:]
        if message.get("role") in {"user", "assistant"}
    ]

    system_prompt = f"""
당신은 K-POP 데이터와 마케팅을 분석하는 AI 애널리스트입니다.

답변 원칙:
1. 한국어로 답합니다.
2. 핵심 결론을 먼저 제시합니다.
3. 제공된 데이터에 근거해 숫자를 구체적으로 활용합니다.
4. 데이터 사실과 해석을 구분합니다.
5. 글로벌 뉴스와 국내 뉴스를 필요할 때 비교합니다.
6. 불확실한 내용은 추정이라고 명확히 표시합니다.
7. 답변은 간결한 소제목과 문단으로 작성합니다.

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
    spotify_data: dict[str, Any],
    youtube_data: list[dict[str, Any]],
    global_news: list[dict[str, Any]],
    naver_news: list[dict[str, Any]],
) -> str:
    album = spotify_data.get("latest_album", {})
    strongest = max(components, key=components.get)
    weakest = min(components, key=components.get)
    top_video = max(youtube_data, key=lambda x: x.get("views", 0), default={})

    return f"""
**{artist_name}의 현재 Comeback Score는 {score}/100점**입니다.

가장 강한 신호는 **{strongest} {components[strongest]}점**, 상대적으로 약한 신호는
**{weakest} {components[weakest]}점**입니다.

- 최신 확인 앨범: **{album.get("name", "정보 없음")}**
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

def render_album_card(artist_name: str, spotify_data: dict[str, Any]) -> None:
    album = spotify_data.get("latest_album", {})
    image_url = album.get("image", "")
    spotify_url = album.get("spotify_url", "")

    image_html = (
        f'<img class="album-cover" src="{escape_text(image_url)}" '
        f'alt="{escape_text(album.get("name"))}">'
        if image_url
        else (
            '<div class="album-cover" style="display:flex;align-items:center;'
            'justify-content:center;font-size:2.1rem;">💿</div>'
        )
    )

    link_html = (
        f'<div style="margin-top:10px;"><a href="{escape_text(spotify_url)}" '
        'target="_blank" style="color:#c4b5fd;text-decoration:none;'
        'font-weight:700;">Spotify에서 열기 ↗</a></div>'
        if spotify_url
        else ""
    )

    st.markdown(
        f"""
        <div class="album-card">
            {image_html}
            <div>
                <div class="muted">{escape_text(artist_name)} · Latest Release</div>
                <div class="album-name">{escape_text(album.get("name", "앨범 정보 없음"))}</div>
                <div class="muted">
                    발매일 {escape_text(format_date(album.get("release_date")))}<br>
                    {escape_text(album.get("album_type", "-"))} ·
                    {escape_text(album.get("total_tracks", 0))} tracks
                </div>
                {link_html}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


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

spotify_client_id = get_secret("SPOTIFY_CLIENT_ID")
spotify_client_secret = get_secret("SPOTIFY_CLIENT_SECRET")
youtube_api_key = get_secret("YOUTUBE_API_KEY")
news_api_key = get_secret("NEWS_API_KEY")
naver_client_id = get_secret("NAVER_CLIENT_ID")
naver_client_secret = get_secret("NAVER_CLIENT_SECRET")
solar_api_key = get_secret("SOLAR_API_KEY")
solar_model = get_secret("SOLAR_MODEL", "solar-pro2")

spotify_connected = bool(spotify_client_id and spotify_client_secret)
youtube_connected = bool(youtube_api_key)
news_connected = bool(news_api_key)
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
    st.write(f"{'🟢' if spotify_connected else '⚪'} Spotify")
    st.write(f"{'🟢' if youtube_connected else '⚪'} YouTube")
    st.write(f"{'🟢' if news_connected else '⚪'} NewsAPI")
    st.write(f"{'🟢' if naver_connected else '⚪'} 네이버 뉴스")
    st.write(f"{'🟢' if solar_connected else '⚪'} Solar AI")

    st.caption("연결되지 않은 API는 데모 데이터 또는 규칙 기반 답변으로 대체됩니다.")

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

spotify_data = demo["spotify"]
youtube_data = demo["youtube"]
global_news = demo["global_news"]
naver_news = demo["naver_news"]

active_sources: list[str] = []
api_errors: list[str] = []

if demo_mode:
    active_sources = [
        "Spotify Demo",
        "YouTube Demo",
        "Global News Demo",
        "Korean News Demo",
    ]
else:
    if spotify_connected:
        try:
            spotify_data = get_spotify_data(
                config["spotify_query"],
                spotify_client_id,
                spotify_client_secret,
            )
            active_sources.append("Spotify Live")
        except RuntimeError as error:
            api_errors.append(f"Spotify: {error}")
            active_sources.append("Spotify Demo")
    else:
        active_sources.append("Spotify Demo")

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
    else:
        active_sources.append("YouTube Demo")

    if news_connected:
        try:
            global_news = get_global_news(
                config["global_news_query"],
                news_api_key,
            )
            active_sources.append("NewsAPI Live")
        except RuntimeError as error:
            api_errors.append(f"NewsAPI: {error}")
            active_sources.append("Global News Demo")
    else:
        active_sources.append("Global News Demo")

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
    else:
        active_sources.append("Korean News Demo")

score, components = calculate_comeback_score(
    spotify_data,
    youtube_data,
    global_news,
    naver_news,
)


# =========================================================
# 15. HEADER / METRICS
# =========================================================

badges = "".join(
    f'<span class="badge">{escape_text(source)}</span>'
    for source in active_sources
)

st.markdown(
    f"""
    <div class="hero">
        <div class="eyebrow">Real-time K-POP Intelligence</div>
        <h1 class="hero-title">K-POP Comeback Radar</h1>
        <div class="hero-subtitle">
            {escape_text(config["emoji"])}
            <strong>{escape_text(selected_artist)}</strong>의
            Spotify·YouTube·글로벌 뉴스·국내 뉴스 신호를 한 화면에서 추적하고,
            Solar AI 애널리스트에게 질문해보세요.
        </div>
        <div style="margin-top:15px;">{badges}</div>
    </div>
    """,
    unsafe_allow_html=True,
)

if api_errors:
    with st.expander(f"⚠️ 일부 API 연결 오류 {len(api_errors)}건"):
        for error in api_errors:
            st.warning(error)

if demo_mode or not all(
    [
        spotify_connected,
        youtube_connected,
        news_connected,
        naver_connected,
    ]
):
    st.info(
        "현재 일부 영역에는 데모 데이터가 포함될 수 있습니다. "
        "Streamlit Secrets에 해당 API 키를 등록하면 실데이터로 전환됩니다."
    )

artist_data = spotify_data.get("artist", {})
top_video = max(youtube_data, key=lambda x: x.get("views", 0), default={})

metric_columns = st.columns(5)
metric_columns[0].metric(
    "Spotify Popularity",
    f"{artist_data.get('popularity', 0)}/100",
)
metric_columns[1].metric(
    "Spotify Followers",
    format_number(artist_data.get("followers", 0)),
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

left, center, right = st.columns([1.35, 1.65, 1.0], gap="large")

with left:
    st.markdown('<div class="section-title">💿 Latest Release</div>', unsafe_allow_html=True)
    render_album_card(selected_artist, spotify_data)

    st.markdown('<div class="section-title">🎧 Spotify Top Tracks</div>', unsafe_allow_html=True)

    tracks_df = pd.DataFrame(spotify_data.get("top_tracks", []))

    if tracks_df.empty:
        st.info("Spotify 인기곡 정보가 없습니다.")
    else:
        chart_df = tracks_df.head(8).sort_values("popularity", ascending=True)

        fig = px.bar(
            chart_df,
            x="popularity",
            y="name",
            orientation="h",
            labels={"popularity": "Spotify Popularity", "name": ""},
            text="popularity",
        )
        fig.update_layout(
            height=390,
            margin=dict(l=0, r=15, t=15, b=0),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#d9dcec"),
            xaxis=dict(
                range=[0, 100],
                gridcolor="rgba(255,255,255,.07)",
            ),
            yaxis=dict(tickfont=dict(size=11)),
        )
        fig.update_traces(
            textposition="outside",
            hovertemplate="<b>%{y}</b><br>Popularity: %{x}<extra></extra>",
        )
        st.plotly_chart(
            fig,
            use_container_width=True,
            config={"displayModeBar": False},
        )

with center:
    st.markdown('<div class="section-title">🎬 YouTube Signal</div>', unsafe_allow_html=True)
    render_youtube_videos(youtube_data)

with right:
    st.markdown('<div class="section-title">📈 Comeback Score</div>', unsafe_allow_html=True)

    st.markdown(
        f"""
        <div class="score-card">
            <div class="muted">현재 레이더 점수</div>
            <div class="score-number">{score:.0f}</div>
            <div style="font-size:1.05rem;font-weight:800;margin-top:9px;">
                {escape_text(score_label(score))}
            </div>
            <div class="muted" style="margin-top:10px;">
                Spotify·발매 시점·YouTube·국내외 뉴스 신호를
                가중 합산한 연습용 지표입니다.
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
    radar_fig.update_traces(fill="toself")
    radar_fig.update_layout(
        height=350,
        margin=dict(l=20, r=20, t=35, b=25),
        paper_bgcolor="rgba(0,0,0,0)",
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                gridcolor="rgba(255,255,255,.10)",
                tickfont=dict(color="#9ba3be"),
            ),
            angularaxis=dict(
                gridcolor="rgba(255,255,255,.10)",
                tickfont=dict(color="#d9dcec", size=11),
            ),
        ),
        showlegend=False,
        font=dict(color="#d9dcec"),
    )
    st.plotly_chart(
        radar_fig,
        use_container_width=True,
        config={"displayModeBar": False},
    )


# =========================================================
# 17. GLOBAL / KOREAN NEWS
# =========================================================

st.markdown("---")
st.markdown('<div class="section-title">📰 Comeback News Monitor</div>', unsafe_allow_html=True)

global_tab, korean_tab = st.tabs(["🌎 Global News", "🇰🇷 Korean News"])

with global_tab:
    st.caption("NewsAPI를 통해 수집한 영문권 기사입니다.")
    render_news_cards(global_news)

with korean_tab:
    st.caption("네이버 검색 API를 통해 수집한 국내 최신 기사입니다.")
    render_news_cards(naver_news)


# =========================================================
# 18. INTERPRETATION
# =========================================================

st.markdown("---")
st.markdown('<div class="section-title">🔍 Radar Interpretation</div>', unsafe_allow_html=True)

strongest = max(components, key=components.get)
weakest = min(components, key=components.get)
release_age = days_since(
    spotify_data.get("latest_album", {}).get("release_date")
)

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
            <h3>{escape_text(strongest)}</h3>
            <div class="muted">
                {components[strongest]:.1f}점으로 현재 네 가지 지표 중 가장 높습니다.
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
            <h3>{escape_text(weakest)}</h3>
            <div class="muted">
                {components[weakest]:.1f}점입니다. 추가 데이터에 따라 달라질 수 있습니다.
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
            <h3>Latest Signal</h3>
            <div class="muted">{escape_text(release_description)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# =========================================================
# 19. SOLAR AI CHAT
# =========================================================

st.markdown("---")
st.markdown('<div class="section-title">🤖 Ask the Solar K-POP Analyst</div>', unsafe_allow_html=True)

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
                    spotify_data,
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
                            spotify_data,
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
                    spotify_data,
                    youtube_data,
                    global_news,
                    naver_news,
                )

        st.markdown(answer)

    st.session_state.chat_messages.append(
        {"role": "assistant", "content": answer}
    )


# =========================================================
# 20. FOOTER
# =========================================================

st.markdown("---")
st.caption(
    "K-POP Comeback Radar MVP · "
    "Spotify Web API · YouTube Data API · NewsAPI · Naver Search API · Upstage Solar · "
    "Comeback Score는 본 프로젝트의 비공식 학습용 지표입니다."
)
