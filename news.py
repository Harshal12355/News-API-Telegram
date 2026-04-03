import os
import logging

import requests
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

logger = logging.getLogger(__name__)

NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

_TOP_HEADLINES = "https://newsapi.org/v2/top-headlines"
_MAX_ARTICLES_FOR_PROMPT = 15


def _client():
    return OpenAI(api_key=OPENAI_API_KEY)


def fetch_news(category: str | None = None):
    """
    Fetch US top headlines. If category is None, returns headlines across all
    categories. Otherwise category must be a NewsAPI value, e.g. general,
    technology, health — not the string \"top-headlines\".
    """
    params = {"country": "us", "apiKey": NEWSAPI_KEY}
    if category:
        params["category"] = category
    response = requests.get(_TOP_HEADLINES, params=params, timeout=30)
    data = response.json()
    if data.get("status") != "ok":
        logger.warning(
            "NewsAPI error: %s",
            data.get("message", data),
        )
        return []
    articles = data.get("articles") or []
    logger.info("Fetched %s articles (category=%s)", len(articles), category)
    return articles


def _articles_to_prompt_text(articles: list, max_items: int = _MAX_ARTICLES_FOR_PROMPT) -> str:
    lines = []
    for i, a in enumerate(articles[:max_items], start=1):
        title = (a.get("title") or "").strip()
        desc = (a.get("description") or "").strip()
        url = (a.get("url") or "").strip()
        published = a.get("publishedAt") or ""
        lines.append(f"{i}. {title}\n   {desc}\n   {url}\n   {published}")
    return "\n".join(lines) if lines else "(No articles returned.)"


def summarise_news(articles: list) -> str:
    if not articles:
        return "No articles to summarize today."

    block = _articles_to_prompt_text(articles)
    prompt = f"""Summarise the following news:

{block}

Break it down into adhd friendly format
and explain it like you are richard feynman.
Rank the news by importance and relevance to the topic of AI
Use Bullet points to list the news in order of importance.

The format of the message needs to be clear and easy to read in telegram."""
    r = _client().chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1000,
    )
    return r.choices[0].message.content
