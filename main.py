from __future__ import annotations

import base64
import html
import math
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
# 2. CONSTANTS
# =========================================================

SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_API_URL = "https://api.spotify.com/v1"

YOUTUBE_API_URL = "https://www.googleapis.com/youtube/v3"

NEWS_API_URL = "https://newsapi.org/v2/everything"


ARTISTS: dict[str, dict[str, str]] = {
    "aespa": {
        "spotify_query": "aespa",
        "youtube_query": "aespa official",
        "news_query": 'aespa OR 에스파',
        "emoji": "🪩",
    },
    "BLACKPINK": {
        "spotify_query": "BLACKPINK",
        "youtube_query": "BLACKPINK official",
        "news_query": 'BLACKPINK OR 블랙핑크',
        "emoji": "🖤",
    },
    "BTS": {
        "spotify_query": "BTS",
        "youtube_query": "BANGTANTV BTS",
        "news_query": 'BTS OR 방탄소년단',
        "emoji": "💜",
    },
    "IVE": {
        "spotify_query": "IVE",
        "youtube_query": "IVE official",
        "news_query": 'IVE OR 아이브',
        "emoji": "✨",
    },
    "LE SSERAFIM": {
        "spotify_query": "LE SSERAFIM",
        "youtube_query": "LE SSERAFIM official",
        "news_query": 'LE SSERAFIM OR 르세라핌',
        "emoji": "🔥",
    },
    "NCT DREAM": {
        "spotify_query": "NCT DREAM",
        "youtube_query": "NCT DREAM official",
        "news_query": '"NCT DREAM" OR 엔시티드림',
        "emoji": "💚",
    },
    "NewJeans": {
        "spotify_query": "NewJeans",
        "youtube_query": "NewJeans official",
        "news_query": 'NewJeans OR 뉴진스',
        "emoji": "🐰",
    },
    "RIIZE": {
        "spotify_query": "RIIZE",
        "youtube_query": "RIIZE official",
        "news_query": 'RIIZE OR 라이즈',
        "emoji": "🌅",
    },
    "SEVENTEEN": {
        "spotify_query": "SEVENTEEN",
        "youtube_query": "SEVENTEEN official",
        "news_query": 'SEVENTEEN OR 세븐틴',
        "emoji": "💎",
    },
    "Stray Kids": {
        "spotify_query": "Stray Kids",
        "youtube_query": "Stray Kids official",
        "news_query": '"Stray Kids" OR 스트레이키즈',
        "emoji": "⚡",
    },
}


# =========================================================
# 3. CUSTOM CSS
# =========================================================

st.markdown(
    """
    <style>
        .stApp {
            background:
                radial-gradient(circle at 15% 10%, rgba(145, 80, 255, 0.16), transparent 26%),
                radial-gradient(circle at 85% 10%, rgba(255, 57, 154, 0.13), transparent 25%),
                linear-gradient(180deg, #090b16 0%, #101427 100%);
            color: #f7f7fb;
        }

        [data-testid="stSidebar"] {
            background: rgba(12, 14, 28, 0.96);
            border-right: 1px solid rgba(255, 255, 255, 0.08);
        }

        .block-container {
            max-width: 1380px;
            padding-top: 2rem;
            padding-bottom: 3rem;
        }

        .radar-hero {
            padding: 28px 30px;
            border: 1px solid rgba(255,255,255,0.10);
            border-radius: 24px;
            background:
                linear-gradient(135deg, rgba(139,92,246,0.20), rgba(236,72,153,0.10)),
                rgba(15,18,35,0.82);
            box-shadow: 0 18px 50px rgba(0,0,0,0.28);
            margin-bottom: 24px;
        }

        .radar-eyebrow {
            color: #c4b5fd;
            font-size: 0.78rem;
            font-weight: 800;
            letter-spacing: 0.18em;
            text-transform: uppercase;
            margin-bottom: 8px;
        }

        .radar-title {
            font-size: clamp(2rem, 4vw, 4rem);
            line-height: 1.02;
            font-weight: 900;
            margin: 0;
            background: linear-gradient(90deg, #ffffff, #d8b4fe, #f9a8d4);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .radar-subtitle {
            color: #b8bfd4;
            margin-top: 13px;
            font-size: 1rem;
            max-width: 820px;
            line-height: 1.65;
        }

        .section-title {
            font-size: 1.35rem;
            font-weight: 850;
            margin-top: 14px;
            margin-bottom: 14px;
        }

        .glass-card {
            height: 100%;
            padding: 20px;
            border-radius: 20px;
            background: rgba(21, 25, 48, 0.86);
            border: 1px solid rgba(255, 255, 255, 0.09);
            box-shadow: 0 12px 35px rgba(0,0,0,0.22);
        }

        .album-card {
            display: flex;
            gap: 18px;
            align-items: center;
            padding: 18px;
            border-radius: 20px;
            background: rgba(21,25,48,0.9);
            border: 1px solid rgba(255,255,255,0.09);
            margin-bottom: 14px;
        }

        .album-cover {
            width: 118px;
            height: 118px;
            min-width: 118px;
            border-radius: 16px;
            object-fit: cover;
            background: #282d4d;
        }

        .album-name {
            font-size: 1.15rem;
            font-weight: 850;
            margin-bottom: 8px;
        }

        .muted {
            color: #aeb5cb;
            font-size: 0.9rem;
            line-height: 1.55;
        }

        .metric-label {
            color: #9da6c4;
            font-size: 0.79rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.06em;
        }

        .metric-value {
            color: white;
            font-size: 1.65rem;
            font-weight: 900;
            margin-top: 6px;
        }

        .score-card {
            text-align: center;
            padding: 26px 18px;
            border-radius: 22px;
            background:
                radial-gradient(circle at 50% 5%, rgba(236,72,153,.23), transparent 42%),
                rgba(21,25,48,.9);
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
            padding: 17px 18px;
            margin-bottom: 12px;
            border-radius: 17px;
            background: rgba(21,25,48,.84);
            border: 1px solid rgba(255,255,255,.08);
        }

        .news-title {
            color: #ffffff;
            font-weight: 800;
            font-size: 0.99rem;
            line-height: 1.45;
            text-decoration: none;
        }

        .news-title:hover {
            color: #d8b4fe;
        }

        .news-meta {
            color: #959db9;
            font-size: .78rem;
            margin-top: 8px;
        }

        .api-badge {
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
            background: rgba(21,25,48,.7);
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
                padding-top: 1rem;
                padding-left: 1rem;
                padding-right: 1rem;
            }

            .radar-hero {
                padding: 22px 20px;
                border-radius: 19px;
            }

            .radar-title {
                font-size: 2.25rem;
            }

            .radar-subtitle {
                font-size: .92rem;
            }

            .album-card {
                align-items: flex-start;
                gap: 13px;
                padding: 14px;
            }

            .album-cover {
                width: 88px;
                height: 88px;
                min-width: 88px;
            }

            .album-name {
                font-size: 1rem;
            }

            .score-number {
                font-size: 3rem;
            }
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# 4. HELPER FUNCTIONS
# =========================================================

def get_secret(name: str, default: str = "") -> str:
    """
    Streamlit secrets에서 값을 안전하게 불러옵니다.
    secrets.toml 자체가 없어도 앱이 중단되지 않습니다.
    """
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
    timeout: int = 15,
) -> dict[str, Any]:
    """
    HTTP 요청을 실행하고 오류 발생 시 이해하기 쉬운 예외를 만듭니다.
    """
    try:
        response = requests.request(
            method=method,
            url=url,
            headers=headers,
            params=params,
            data=data,
            timeout=timeout,
        )
        response.raise_for_status()
        return response.json()

    except requests.exceptions.Timeout as exc:
        raise RuntimeError("API 응답 시간이 초과되었습니다.") from exc

    except requests.exceptions.HTTPError as exc:
        status_code = exc.response.status_code if exc.response else "unknown"

        try:
            detail = exc.response.json()
        except Exception:
            detail = exc.response.text[:300] if exc.response else ""

        raise RuntimeError(
            f"API 요청 오류가 발생했습니다. 상태 코드: {status_code}, 상세: {detail}"
        ) from exc

    except requests.exceptions.RequestException as exc:
        raise RuntimeError(f"네트워크 요청에 실패했습니다: {exc}") from exc


def escape_text(value: Any) -> str:
    return html.escape(str(value or ""))


def parse_iso_datetime(value: str | None) -> datetime | None:
    if not value:
        return None

    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def format_date(value: str | None) -> str:
    parsed = parse_iso_datetime(value)

    if parsed:
        return parsed.astimezone().strftime("%Y.%m.%d")

    if value:
        return value.replace("-", ".")

    return "-"


def days_since(value: str | None) -> int | None:
    parsed = parse_iso_datetime(value)

    if parsed is None and value:
        try:
            parsed = datetime.strptime(value, "%Y-%m-%d").replace(
                tzinfo=timezone.utc
            )
        except ValueError:
            return None

    if parsed is None:
        return None

    now = datetime.now(timezone.utc)
    return max((now - parsed.astimezone(timezone.utc)).days, 0)


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
    """
    1억 회 이상이면 100점에 가까워지는 로그 스케일입니다.
    """
    try:
        views = max(float(value or 0), 0)
    except (TypeError, ValueError):
        views = 0

    if views <= 0:
        return 0.0

    return min(math.log10(views + 1) / 8 * 100, 100)


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


def get_score_label(score: float) -> str:
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
# 5. SPOTIFY API
# =========================================================

@st.cache_data(ttl=300, show_spinner=False)
def get_spotify_token(client_id: str, client_secret: str) -> str:
    credentials = f"{client_id}:{client_secret}"
    encoded_credentials = base64.b64encode(
        credentials.encode("utf-8")
    ).decode("utf-8")

    payload = safe_request(
        "POST",
        SPOTIFY_TOKEN_URL,
        headers={
            "Authorization": f"Basic {encoded_credentials}",
            "Content-Type": "application/x-www-form-urlencoded",
        },
        data={"grant_type": "client_credentials"},
    )

    token = payload.get("access_token")

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
        params={
            "q": artist_query,
            "type": "artist",
            "limit": 5,
        },
    )

    artists = search_result.get("artists", {}).get("items", [])

    if not artists:
        raise RuntimeError("Spotify에서 아티스트를 찾지 못했습니다.")

    exact_artist = next(
        (
            artist
            for artist in artists
            if artist.get("name", "").lower() == artist_query.lower()
        ),
        artists[0],
    )

    artist_id = exact_artist["id"]

    top_tracks_result = safe_request(
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
            "limit": 20,
        },
    )

    albums = albums_result.get("items", [])

    # 동일 앨범이 국가·버전별로 중복되는 경우를 제거합니다.
    unique_albums: list[dict[str, Any]] = []
    seen_album_names: set[str] = set()

    for album in albums:
        album_name = album.get("name", "").strip().lower()

        if album_name and album_name not in seen_album_names:
            seen_album_names.add(album_name)
            unique_albums.append(album)

    unique_albums.sort(
        key=lambda item: item.get("release_date", ""),
        reverse=True,
    )

    latest_album = unique_albums[0] if unique_albums else {}

    artist_images = exact_artist.get("images", [])
    album_images = latest_album.get("images", [])

    return {
        "artist": {
            "id": artist_id,
            "name": exact_artist.get("name", artist_query),
            "followers": exact_artist.get("followers", {}).get("total", 0),
            "popularity": exact_artist.get("popularity", 0),
            "genres": exact_artist.get("genres", []),
            "image": artist_images[0]["url"] if artist_images else "",
            "spotify_url": exact_artist.get(
                "external_urls", {}
            ).get("spotify", ""),
        },
        "latest_album": {
            "name": latest_album.get("name", "앨범 정보 없음"),
            "release_date": latest_album.get("release_date", ""),
            "album_type": latest_album.get("album_type", ""),
            "total_tracks": latest_album.get("total_tracks", 0),
            "image": album_images[0]["url"] if album_images else "",
            "spotify_url": latest_album.get(
                "external_urls", {}
            ).get("spotify", ""),
        },
        "top_tracks": [
            {
                "name": track.get("name", ""),
                "popularity": track.get("popularity", 0),
                "album": track.get("album", {}).get("name", ""),
                "spotify_url": track.get(
                    "external_urls", {}
                ).get("spotify", ""),
            }
            for track in top_tracks_result.get("tracks", [])[:10]
        ],
    }


# =========================================================
# 6. YOUTUBE API
# =========================================================

@st.cache_data(ttl=1800, show_spinner=False)
def get_youtube_data(
    search_query: str,
    api_key: str,
) -> list[dict[str, Any]]:
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

    statistics_result = safe_request(
        "GET",
        f"{YOUTUBE_API_URL}/videos",
        params={
            "part": "snippet,statistics",
            "id": ",".join(video_ids),
            "key": api_key,
        },
    )

    videos: list[dict[str, Any]] = []

    for item in statistics_result.get("items", []):
        snippet = item.get("snippet", {})
        statistics = item.get("statistics", {})
        thumbnails = snippet.get("thumbnails", {})

        thumbnail = (
            thumbnails.get("high", {}).get("url")
            or thumbnails.get("medium", {}).get("url")
            or thumbnails.get("default", {}).get("url")
            or ""
        )

        video_id = item.get("id", "")

        videos.append(
            {
                "video_id": video_id,
                "title": snippet.get("title", ""),
                "published_at": snippet.get("publishedAt", ""),
                "channel_title": snippet.get("channelTitle", ""),
                "thumbnail": thumbnail,
                "views": int(statistics.get("viewCount", 0)),
                "likes": int(statistics.get("likeCount", 0)),
                "comments": int(statistics.get("commentCount", 0)),
                "url": f"https://www.youtube.com/watch?v={video_id}",
            }
        )

    videos.sort(
        key=lambda video: video.get("published_at", ""),
        reverse=True,
    )

    return videos


# =========================================================
# 7. NEWS API
# =========================================================

@st.cache_data(ttl=1800, show_spinner=False)
def get_news_data(
    query: str,
    api_key: str,
) -> list[dict[str, Any]]:
    news_result = safe_request(
        "GET",
        NEWS_API_URL,
        params={
            "q": query,
            "language": "en",
            "sortBy": "publishedAt",
            "pageSize": 10,
            "apiKey": api_key,
        },
    )

    articles = news_result.get("articles", [])

    return [
        {
            "title": article.get("title", ""),
            "description": article.get("description", ""),
            "source": article.get("source", {}).get("name", ""),
            "published_at": article.get("publishedAt", ""),
            "url": article.get("url", ""),
            "image": article.get("urlToImage", ""),
        }
        for article in articles
        if article.get("title") and article.get("url")
    ]


# =========================================================
# 8. DEMO DATA
# =========================================================

def get_demo_data(artist_name: str) -> dict[str, Any]:
    """
    API 키가 없을 때 UI와 분석 흐름을 확인하기 위한 예시 데이터입니다.
    실제 최신 데이터가 아닙니다.
    """
    artist_info = ARTISTS[artist_name]

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
                {
                    "name": "Demo Track A",
                    "popularity": 91,
                    "album": "Demo Album",
                    "spotify_url": "",
                },
                {
                    "name": "Demo Track B",
                    "popularity": 86,
                    "album": "Demo Album",
                    "spotify_url": "",
                },
                {
                    "name": "Demo Track C",
                    "popularity": 79,
                    "album": "Demo Album",
                    "spotify_url": "",
                },
                {
                    "name": "Demo Track D",
                    "popularity": 73,
                    "album": "Demo Album",
                    "spotify_url": "",
                },
                {
                    "name": "Demo Track E",
                    "popularity": 67,
                    "album": "Demo Album",
                    "spotify_url": "",
                },
            ],
        },
        "youtube": [
            {
                "video_id": "demo1",
                "title": f"{artist_name} Official MV — Demo",
                "published_at": datetime.now(timezone.utc).isoformat(),
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
                "published_at": datetime.now(timezone.utc).isoformat(),
                "channel_title": f"{artist_name} Official",
                "thumbnail": "",
                "views": 11_300_000,
                "likes": 820_000,
                "comments": 74_000,
                "url": "",
            },
        ],
        "news": [
            {
                "title": f"{artist_name}, 글로벌 컴백 관심도 상승",
                "description": "API 키가 없을 때 표시되는 데모 뉴스입니다.",
                "source": "Demo News",
                "published_at": datetime.now(timezone.utc).isoformat(),
                "url": "",
                "image": "",
            },
            {
                "title": f"팬들이 주목하는 {artist_name}의 새로운 콘셉트",
                "description": "실제 데이터 연결 후 최근 기사로 대체됩니다.",
                "source": "Demo Magazine",
                "published_at": datetime.now(timezone.utc).isoformat(),
                "url": "",
                "image": "",
            },
        ],
        "emoji": artist_info["emoji"],
    }


# =========================================================
# 9. COMEBACK SCORE
# =========================================================

def calculate_comeback_score(
    spotify_data: dict[str, Any],
    youtube_data: list[dict[str, Any]],
    news_data: list[dict[str, Any]],
) -> tuple[float, dict[str, float]]:
    artist_popularity = normalize_popularity(
        spotify_data.get("artist", {}).get("popularity", 0)
    )

    release_freshness = freshness_score(
        spotify_data.get("latest_album", {}).get("release_date")
    )

    top_video_views = max(
        (video.get("views", 0) for video in youtube_data),
        default=0,
    )
    youtube_score = normalize_youtube_views(top_video_views)

    recent_news_count = 0

    for article in news_data:
        age = days_since(article.get("published_at"))

        if age is not None and age <= 30:
            recent_news_count += 1

    news_score = min(recent_news_count / 10 * 100, 100)

    # MVP 가중치
    components = {
        "Spotify 인기도": round(artist_popularity, 1),
        "발매 최신성": round(release_freshness, 1),
        "YouTube 반응": round(youtube_score, 1),
        "뉴스 화제성": round(news_score, 1),
    }

    total_score = (
        components["Spotify 인기도"] * 0.30
        + components["발매 최신성"] * 0.30
        + components["YouTube 반응"] * 0.25
        + components["뉴스 화제성"] * 0.15
    )

    return round(total_score, 1), components


# =========================================================
# 10. AI CHAT
# =========================================================

def build_ai_context(
    artist_name: str,
    spotify_data: dict[str, Any],
    youtube_data: list[dict[str, Any]],
    news_data: list[dict[str, Any]],
    score: float,
    score_components: dict[str, float],
) -> str:
    artist = spotify_data.get("artist", {})
    album = spotify_data.get("latest_album", {})
    tracks = spotify_data.get("top_tracks", [])

    track_text = "\n".join(
        [
            f"- {track.get('name')} / popularity {track.get('popularity')}"
            for track in tracks[:5]
        ]
    )

    youtube_text = "\n".join(
        [
            (
                f"- {video.get('title')} / "
                f"views {video.get('views', 0):,} / "
                f"published {format_date(video.get('published_at'))}"
            )
            for video in youtube_data[:5]
        ]
    )

    news_text = "\n".join(
        [
            (
                f"- {article.get('title')} / "
                f"{article.get('source')} / "
                f"{format_date(article.get('published_at'))}"
            )
            for article in news_data[:6]
        ]
    )

    return f"""
분석 대상: {artist_name}

[Spotify 데이터]
아티스트 인기도: {artist.get('popularity', 0)}
팔로워: {artist.get('followers', 0):,}
장르: {', '.join(artist.get('genres', []))}
최신 앨범: {album.get('name')}
발매일: {album.get('release_date')}
트랙 수: {album.get('total_tracks')}

인기곡:
{track_text or '- 데이터 없음'}

[YouTube 데이터]
{youtube_text or '- 데이터 없음'}

[최근 뉴스]
{news_text or '- 데이터 없음'}

[Comeback Score]
총점: {score}/100
세부 점수: {score_components}

주의:
- 제공된 데이터에 없는 사실을 확정적으로 만들어내지 않는다.
- 조회수와 인기도는 수집 시점의 값이라고 설명한다.
- 인과관계가 입증되지 않은 경우 '가능성이 있다', '추정된다'라고 표현한다.
""".strip()


def ask_openai(
    api_key: str,
    model: str,
    user_question: str,
    data_context: str,
    chat_history: list[dict[str, str]],
) -> str:
    """
    openai 패키지에 의존하지 않고 HTTP API로 호출합니다.
    requirements.txt를 단순하게 유지하기 위한 구성입니다.
    """
    recent_history = chat_history[-6:]

    history_text = "\n".join(
        [
            f"{message['role']}: {message['content']}"
            for message in recent_history
        ]
    )

    prompt = f"""
당신은 K-POP 데이터와 마케팅을 분석하는 AI 애널리스트입니다.

답변 원칙:
1. 한국어로 답변합니다.
2. 핵심 결론을 먼저 말합니다.
3. 반드시 아래 제공된 데이터에 근거합니다.
4. 데이터와 해석을 구분합니다.
5. 불확실한 내용은 추정이라고 밝힙니다.
6. 숫자를 활용해 구체적으로 설명합니다.
7. 답변은 지나치게 길지 않게 작성합니다.

현재 데이터:
{data_context}

최근 대화:
{history_text}

사용자 질문:
{user_question}
""".strip()

    payload = {
        "model": model,
        "input": prompt,
    }

    try:
        response = requests.post(
            "https://api.openai.com/v1/responses",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json=payload,
            timeout=40,
        )
        response.raise_for_status()
        result = response.json()

    except requests.exceptions.RequestException as exc:
        raise RuntimeError(f"OpenAI API 호출에 실패했습니다: {exc}") from exc

    # Responses API의 output_text가 제공되는 경우
    if result.get("output_text"):
        return str(result["output_text"]).strip()

    # 일부 응답 구조를 대비한 fallback
    output_parts: list[str] = []

    for output_item in result.get("output", []):
        for content_item in output_item.get("content", []):
            if content_item.get("type") in {"output_text", "text"}:
                text_value = content_item.get("text", "")

                if isinstance(text_value, dict):
                    text_value = text_value.get("value", "")

                if text_value:
                    output_parts.append(str(text_value))

    if output_parts:
        return "\n".join(output_parts).strip()

    raise RuntimeError("OpenAI 응답에서 텍스트를 찾지 못했습니다.")


def generate_rule_based_answer(
    artist_name: str,
    question: str,
    score: float,
    score_components: dict[str, float],
    spotify_data: dict[str, Any],
    youtube_data: list[dict[str, Any]],
    news_data: list[dict[str, Any]],
) -> str:
    """
    OpenAI API 키가 없는 경우 사용하는 간단한 분석 답변입니다.
    """
    album = spotify_data.get("latest_album", {})
    top_video = max(
        youtube_data,
        key=lambda video: video.get("views", 0),
        default={},
    )

    strongest_factor = max(
        score_components,
        key=score_components.get,
    )

    weakest_factor = min(
        score_components,
        key=score_components.get,
    )

    return f"""
**{artist_name}의 현재 Comeback Score는 {score}/100점**이며,  
가장 강한 신호는 **{strongest_factor} {score_components[strongest_factor]}점**입니다.

- 최신 확인 앨범: **{album.get("name", "정보 없음")}**
- 발매일: **{format_date(album.get("release_date"))}**
- 가장 조회수가 높은 최근 영상: **{top_video.get("title", "정보 없음")}**
- 해당 영상 조회수: **{format_number(top_video.get("views", 0))}**
- 수집된 최근 뉴스: **{len(news_data)}건**

현재 상대적으로 약한 지표는 **{weakest_factor}**입니다. 따라서 “{question}”에 대한 초기 판단은  
**{strongest_factor}가 관심도를 끌고 있지만, {weakest_factor}를 함께 확인해야 컴백 성과를 더 정확히 평가할 수 있다**는 것입니다.

※ 현재 답변은 OpenAI API가 연결되지 않아 규칙 기반으로 생성되었습니다.
""".strip()


# =========================================================
# 11. RENDER FUNCTIONS
# =========================================================

def render_album_card(
    artist_name: str,
    spotify_data: dict[str, Any],
) -> None:
    album = spotify_data.get("latest_album", {})
    image_url = album.get("image", "")
    spotify_url = album.get("spotify_url", "")

    if image_url:
        image_html = (
            f'<img class="album-cover" src="{escape_text(image_url)}" '
            f'alt="{escape_text(album.get("name"))}">'
        )
    else:
        image_html = """
            <div class="album-cover"
                 style="display:flex;align-items:center;justify-content:center;
                        font-size:2.1rem;">💿</div>
        """

    album_name = escape_text(album.get("name", "앨범 정보 없음"))
    release_date = escape_text(format_date(album.get("release_date")))
    total_tracks = escape_text(album.get("total_tracks", 0))
    album_type = escape_text(album.get("album_type", "-"))

    link_html = ""

    if spotify_url:
        link_html = (
            f'<div style="margin-top:10px;">'
            f'<a href="{escape_text(spotify_url)}" target="_blank" '
            f'style="color:#c4b5fd;text-decoration:none;font-weight:700;">'
            f'Spotify에서 열기 ↗</a></div>'
        )

    st.markdown(
        f"""
        <div class="album-card">
            {image_html}
            <div>
                <div class="muted">{escape_text(artist_name)} · Latest Release</div>
                <div class="album-name">{album_name}</div>
                <div class="muted">
                    발매일 {release_date}<br>
                    {album_type} · {total_tracks} tracks
                </div>
                {link_html}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_news_cards(news_data: list[dict[str, Any]]) -> None:
    if not news_data:
        st.info("표시할 뉴스가 없습니다.")
        return

    for article in news_data[:8]:
        title = escape_text(article.get("title", "제목 없음"))
        source = escape_text(article.get("source", "출처 미상"))
        published_at = escape_text(
            format_date(article.get("published_at"))
        )
        url = article.get("url", "")

        if url:
            title_html = (
                f'<a class="news-title" href="{escape_text(url)}" '
                f'target="_blank">{title}</a>'
            )
        else:
            title_html = f'<div class="news-title">{title}</div>'

        st.markdown(
            f"""
            <div class="news-card">
                {title_html}
                <div class="news-meta">{source} · {published_at}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_youtube_videos(
    videos: list[dict[str, Any]],
) -> None:
    if not videos:
        st.info("표시할 YouTube 영상이 없습니다.")
        return

    for index, video in enumerate(videos[:4]):
        with st.container(border=True):
            left, right = st.columns([1.15, 2.3])

            with left:
                thumbnail = video.get("thumbnail")

                if thumbnail:
                    st.image(thumbnail, use_container_width=True)
                else:
                    st.markdown("### 🎬")

            with right:
                title = video.get("title", "제목 없음")
                url = video.get("url", "")

                if url:
                    st.markdown(f"**[{title}]({url})**")
                else:
                    st.markdown(f"**{title}**")

                st.caption(
                    f"{video.get('channel_title', '')} · "
                    f"{format_date(video.get('published_at'))}"
                )

                metric_columns = st.columns(3)

                metric_columns[0].metric(
                    "조회수",
                    format_number(video.get("views", 0)),
                )
                metric_columns[1].metric(
                    "좋아요",
                    format_number(video.get("likes", 0)),
                )
                metric_columns[2].metric(
                    "댓글",
                    format_number(video.get("comments", 0)),
                )


# =========================================================
# 12. SIDEBAR
# =========================================================

spotify_client_id = get_secret("SPOTIFY_CLIENT_ID")
spotify_client_secret = get_secret("SPOTIFY_CLIENT_SECRET")
youtube_api_key = get_secret("YOUTUBE_API_KEY")
news_api_key = get_secret("NEWS_API_KEY")
openai_api_key = get_secret("OPENAI_API_KEY")
openai_model = get_secret("OPENAI_MODEL", "gpt-4.1-mini")


with st.sidebar:
    st.markdown("## 📡 Radar Control")

    selected_artist = st.selectbox(
        "분석할 아티스트",
        options=list(ARTISTS.keys()),
        index=0,
    )

    st.markdown("---")

    st.markdown("### 데이터 연결 상태")

    spotify_connected = bool(
        spotify_client_id and spotify_client_secret
    )
    youtube_connected = bool(youtube_api_key)
    news_connected = bool(news_api_key)
    openai_connected = bool(openai_api_key)

    st.write(
        f"{'🟢' if spotify_connected else '⚪'} Spotify"
    )
    st.write(
        f"{'🟢' if youtube_connected else '⚪'} YouTube"
    )
    st.write(
        f"{'🟢' if news_connected else '⚪'} NewsAPI"
    )
    st.write(
        f"{'🟢' if openai_connected else '⚪'} OpenAI"
    )

    st.caption(
        "연결되지 않은 API는 데모 데이터 또는 규칙 기반 분석으로 대체됩니다."
    )

    st.markdown("---")

    refresh_clicked = st.button(
        "🔄 데이터 새로고침",
        use_container_width=True,
    )

    if refresh_clicked:
        st.cache_data.clear()
        st.rerun()

    demo_mode_forced = st.toggle(
        "데모 모드 강제 사용",
        value=False,
        help="API 키가 있어도 샘플 데이터로 화면을 확인합니다.",
    )


# =========================================================
# 13. LOAD DATA
# =========================================================

artist_config = ARTISTS[selected_artist]
demo_bundle = get_demo_data(selected_artist)

spotify_data = demo_bundle["spotify"]
youtube_data = demo_bundle["youtube"]
news_data = demo_bundle["news"]

api_errors: list[str] = []
active_sources: list[str] = []


if not demo_mode_forced:
    if spotify_connected:
        try:
            spotify_data = get_spotify_data(
                artist_config["spotify_query"],
                spotify_client_id,
                spotify_client_secret,
            )
            active_sources.append("Spotify Live")
        except RuntimeError as error:
            api_errors.append(f"Spotify: {error}")
    else:
        active_sources.append("Spotify Demo")

    if youtube_connected:
        try:
            youtube_data = get_youtube_data(
                artist_config["youtube_query"],
                youtube_api_key,
            )
            active_sources.append("YouTube Live")
        except RuntimeError as error:
            api_errors.append(f"YouTube: {error}")
    else:
        active_sources.append("YouTube Demo")

    if news_connected:
        try:
            news_data = get_news_data(
                artist_config["news_query"],
                news_api_key,
            )
            active_sources.append("NewsAPI Live")
        except RuntimeError as error:
            api_errors.append(f"NewsAPI: {error}")
    else:
        active_sources.append("News Demo")

else:
    active_sources = [
        "Spotify Demo",
        "YouTube Demo",
        "News Demo",
    ]


score, score_components = calculate_comeback_score(
    spotify_data,
    youtube_data,
    news_data,
)


# =========================================================
# 14. HEADER
# =========================================================

artist_emoji = artist_config["emoji"]

st.markdown(
    f"""
    <div class="radar-hero">
        <div class="radar-eyebrow">Real-time K-POP Intelligence</div>
        <h1 class="radar-title">K-POP Comeback Radar</h1>
        <div class="radar-subtitle">
            {escape_text(artist_emoji)} <strong>{escape_text(selected_artist)}</strong>의
            음악·영상·뉴스 신호를 한 화면에서 추적하고,
            데이터 기반 AI 애널리스트에게 질문해보세요.
        </div>
        <div style="margin-top:15px;">
            {''.join(
                f'<span class="api-badge">{escape_text(source)}</span>'
                for source in active_sources
            )}
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


if api_errors:
    with st.expander(
        f"⚠️ 일부 API 연결 오류 {len(api_errors)}건",
        expanded=False,
    ):
        for api_error in api_errors:
            st.warning(api_error)


if demo_mode_forced or not (
    spotify_connected and youtube_connected and news_connected
):
    st.info(
        "현재 일부 데이터는 데모 데이터입니다. "
        "Streamlit Secrets에 API 키를 등록하면 실제 데이터로 자동 전환됩니다."
    )


# =========================================================
# 15. SUMMARY METRICS
# =========================================================

artist_data = spotify_data.get("artist", {})
album_data = spotify_data.get("latest_album", {})

top_youtube_video = max(
    youtube_data,
    key=lambda video: video.get("views", 0),
    default={},
)

metric_columns = st.columns(4)

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
    format_number(top_youtube_video.get("views", 0)),
)

metric_columns[3].metric(
    "Recent News",
    f"{len(news_data)}건",
)


# =========================================================
# 16. MAIN DASHBOARD
# =========================================================

left_column, center_column, right_column = st.columns(
    [1.35, 1.65, 1.0],
    gap="large",
)


with left_column:
    st.markdown(
        '<div class="section-title">💿 Latest Release</div>',
        unsafe_allow_html=True,
    )

    render_album_card(selected_artist, spotify_data)

    st.markdown(
        '<div class="section-title">🎧 Spotify Top Tracks</div>',
        unsafe_allow_html=True,
    )

    track_dataframe = pd.DataFrame(
        spotify_data.get("top_tracks", [])
    )

    if not track_dataframe.empty:
        chart_dataframe = track_dataframe.head(8).copy()
        chart_dataframe = chart_dataframe.sort_values(
            "popularity",
            ascending=True,
        )

        figure = px.bar(
            chart_dataframe,
            x="popularity",
            y="name",
            orientation="h",
            labels={
                "popularity": "Spotify Popularity",
                "name": "",
            },
            text="popularity",
        )

        figure.update_layout(
            height=390,
            margin=dict(l=0, r=15, t=15, b=0),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#d9dcec"),
            xaxis=dict(range=[0, 100], gridcolor="rgba(255,255,255,.07)"),
            yaxis=dict(tickfont=dict(size=11)),
        )

        figure.update_traces(
            textposition="outside",
            hovertemplate=(
                "<b>%{y}</b><br>"
                "Popularity: %{x}<extra></extra>"
            ),
        )

        st.plotly_chart(
            figure,
            use_container_width=True,
            config={"displayModeBar": False},
        )

    else:
        st.info("Spotify 인기곡 정보가 없습니다.")


with center_column:
    st.markdown(
        '<div class="section-title">🎬 YouTube Signal</div>',
        unsafe_allow_html=True,
    )

    render_youtube_videos(youtube_data)


with right_column:
    st.markdown(
        '<div class="section-title">📈 Comeback Score</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="score-card">
            <div class="muted">현재 레이더 점수</div>
            <div class="score-number">{score:.0f}</div>
            <div style="font-size:1.05rem;font-weight:800;margin-top:9px;">
                {escape_text(get_score_label(score))}
            </div>
            <div class="muted" style="margin-top:10px;">
                Spotify·발매일·YouTube·뉴스 신호를
                가중 합산한 연습용 지표입니다.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    score_dataframe = pd.DataFrame(
        {
            "지표": list(score_components.keys()),
            "점수": list(score_components.values()),
        }
    )

    radar_figure = px.line_polar(
        score_dataframe,
        r="점수",
        theta="지표",
        line_close=True,
        range_r=[0, 100],
    )

    radar_figure.update_traces(fill="toself")

    radar_figure.update_layout(
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
        radar_figure,
        use_container_width=True,
        config={"displayModeBar": False},
    )


# =========================================================
# 17. NEWS
# =========================================================

st.markdown("---")

news_column, insight_column = st.columns(
    [1.25, 1],
    gap="large",
)

with news_column:
    st.markdown(
        '<div class="section-title">📰 Recent News</div>',
        unsafe_allow_html=True,
    )
    render_news_cards(news_data)


with insight_column:
    st.markdown(
        '<div class="section-title">🔍 Radar Interpretation</div>',
        unsafe_allow_html=True,
    )

    strongest_factor = max(
        score_components,
        key=score_components.get,
    )
    weakest_factor = min(
        score_components,
        key=score_components.get,
    )

    release_age = days_since(album_data.get("release_date"))

    if release_age is None:
        release_description = "발매일을 확인할 수 없습니다."
    elif release_age == 0:
        release_description = "오늘 공개된 발매작이 감지되었습니다."
    else:
        release_description = f"최근 발매작은 약 {release_age}일 전 공개됐습니다."

    st.markdown(
        f"""
        <div class="glass-card">
            <div class="metric-label">Strongest Signal</div>
            <div class="metric-value">{escape_text(strongest_factor)}</div>
            <div class="muted">
                현재 {score_components[strongest_factor]:.1f}점으로
                네 가지 분석 지표 중 가장 높습니다.
            </div>

            <br>

            <div class="metric-label">Needs Monitoring</div>
            <div class="metric-value">{escape_text(weakest_factor)}</div>
            <div class="muted">
                현재 {score_components[weakest_factor]:.1f}점입니다.
                데이터가 더 누적되면 점수가 달라질 수 있습니다.
            </div>

            <br>

            <div class="metric-label">Release Timing</div>
            <div class="muted" style="margin-top:8px;">
                {escape_text(release_description)}
            </div>

            <br>

            <div class="metric-label">Interpretation Note</div>
            <div class="muted" style="margin-top:8px;">
                이 점수는 공식 차트나 매출 순위가 아니라,
                API 데이터를 활용해 만든 학습용 자체 지표입니다.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# =========================================================
# 18. AI CHAT
# =========================================================

st.markdown("---")

st.markdown(
    '<div class="section-title">🤖 Ask the K-POP AI Analyst</div>',
    unsafe_allow_html=True,
)

st.caption(
    "예: 이번 컴백의 가장 강한 신호는 무엇이야? · "
    "YouTube 반응과 Spotify 인기도를 비교해줘 · "
    "마케팅 관점에서 어떤 전략이 필요할까?"
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
                f"{selected_artist}의 컴백 데이터를 분석하고 있어요. "
                "궁금한 내용을 질문해주세요."
            ),
        }
    ]


for message in st.session_state.chat_messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


user_question = st.chat_input(
    f"{selected_artist}에 대해 질문해보세요"
)


if user_question:
    st.session_state.chat_messages.append(
        {
            "role": "user",
            "content": user_question,
        }
    )

    with st.chat_message("user"):
        st.markdown(user_question)

    with st.chat_message("assistant"):
        with st.spinner("데이터를 분석하고 있습니다..."):
            if openai_connected and not demo_mode_forced:
                ai_context = build_ai_context(
                    selected_artist,
                    spotify_data,
                    youtube_data,
                    news_data,
                    score,
                    score_components,
                )

                try:
                    answer = ask_openai(
                        api_key=openai_api_key,
                        model=openai_model,
                        user_question=user_question,
                        data_context=ai_context,
                        chat_history=st.session_state.chat_messages,
                    )

                except RuntimeError as error:
                    answer = (
                        f"OpenAI API 연결 중 오류가 발생했습니다.\n\n"
                        f"`{error}`\n\n"
                        "대신 규칙 기반 분석을 제공합니다.\n\n"
                    )

                    answer += generate_rule_based_answer(
                        selected_artist,
                        user_question,
                        score,
                        score_components,
                        spotify_data,
                        youtube_data,
                        news_data,
                    )

            else:
                answer = generate_rule_based_answer(
                    selected_artist,
                    user_question,
                    score,
                    score_components,
                    spotify_data,
                    youtube_data,
                    news_data,
                )

        st.markdown(answer)

    st.session_state.chat_messages.append(
        {
            "role": "assistant",
            "content": answer,
        }
    )


# =========================================================
# 19. FOOTER
# =========================================================

st.markdown("---")

st.caption(
    "K-POP Comeback Radar MVP · "
    "데이터 출처: Spotify Web API, YouTube Data API, NewsAPI · "
    "Comeback Score는 본 프로젝트에서 정의한 비공식 학습용 지표입니다."
)
