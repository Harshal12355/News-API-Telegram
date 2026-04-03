# News API → AI summary → Telegram

A small Python project that pulls US news from [NewsAPI.org](https://newsapi.org/), summarizes it with OpenAI (`gpt-4o-mini`), and sends three digests to Telegram: **Top Headlines** (all categories), **Technology**, and **Health**.

A **GitHub Actions** workflow runs the same script on a daily schedule so you get a morning briefing without hosting a server.

---

## What it does

1. **Fetch** – Calls NewsAPI `top-headlines` for `country=us` three times:
   - No category → broad US top headlines  
   - `technology` → tech category  
   - `health` → health category  

2. **Summarize** – For each batch, sends up to **15 articles** (title, description, URL, published time) to the model with a prompt tuned for short, Telegram-friendly bullets (“ADHD-friendly,” Feynman-style explanation, ranked by relevance to AI).

3. **Deliver** – Sends three separate Telegram messages via the [Bot API](https://core.telegram.org/bots/api) (`sendMessage`, Markdown parse mode).

---

## Project layout

| File | Role |
|------|------|
| `main.py` | Orchestrates fetch → summarize → send; enables logging. |
| `news.py` | `fetch_news(category)`, `summarise_news(articles)`; no network work on import. |
| `telegram.py` | `send_message(text)`. |
| `.github/workflows/daily-news.yml` | Scheduled CI run + manual trigger. |
| `plan.md` | Original learning plan / roadmap ideas. |

---

## Local setup

**Requirements:** Python 3.12+ (matches the workflow).

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Create a `.env` file in the project root (do not commit it):

| Variable | Purpose |
|----------|---------|
| `NEWSAPI_KEY` | NewsAPI.org API key |
| `OPENAI_API_KEY` | OpenAI API key |
| `TELEGRAM_BOT_TOKEN` | From [@BotFather](https://t.me/BotFather) |
| `TELEGRAM_CHAT_ID` | Your chat ID (or group/channel ID the bot can message) |

Run once:

```bash
python main.py
```

---

## GitHub Actions (daily digest)

The workflow **Daily News to Telegram**:

- **Schedule:** **9:20 AM** in **`America/New_York`** (Eastern Time, including EST/EDT), every day.  
  Using an explicit timezone avoids the mistake of a single fixed UTC cron, which does not match “9 AM Eastern” all year.
- **Manual run:** Actions → *Daily News to Telegram* → **Run workflow**.

**Repository secrets** (Settings → Secrets and variables → Actions):

- `NEWSAPI_KEY`
- `OPENAI_API_KEY`
- `TELEGRAM_BOT_TOKEN`
- `TELEGRAM_CHAT_ID`

The workflow must live on the **default branch** for schedules to run. On **public** repos, GitHub can **disable** scheduled workflows after **60 days** without activity; re-enable them under the workflow’s menu if needed. Runs can be **delayed a few minutes** at busy times (GitHub limitation).

---

## Design choices & fixes applied

- **No import-time fetching** – News is loaded only when `main()` runs, not when importing `news.py` (avoids duplicate API calls and surprises in tests).
- **Valid NewsAPI usage** – `category` must be a real value (`technology`, `health`, etc.) or omitted; the invalid value `top-headlines` is not a NewsAPI category.
- **`fetch_news` returns article lists** – The summarizer receives `articles` only, not the raw `status` / `totalResults` wrapper.
- **Bounded prompt size** – At most 15 articles per section, structured as numbered lines for the model.
- **Empty sections** – If a fetch fails or returns no articles, the user-facing text explains that instead of calling OpenAI with junk input.
- **Logging** – INFO-level logs for article counts; warnings when NewsAPI returns an error payload.

---

## Known limitations

- **Telegram** – Messages are capped at **4096** characters; very long model outputs are not auto-split. **`Markdown`** parse mode can error if the model emits unescaped `_`, `*`, etc.
- **NewsAPI** – Free/developer tier limits apply; `top-headlines` does not support the same options as the `everything` endpoint.

---

## Dependencies

See `requirements.txt`: `requests`, `python-dotenv`, and `openai`. Telegram is called with `requests`, not the optional `telegram` Python package.
