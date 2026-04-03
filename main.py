import logging

from news import fetch_news, summarise_news
from telegram import send_message

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")


def main():
    # No category = all top headlines for country (see NewsAPI top-headlines docs).
    top_headlines = fetch_news(None)
    technology = fetch_news("technology")
    health = fetch_news("health")

    body = summarise_news(top_headlines)
    send_message(f"Top Headlines\n\n{body}")
    body = summarise_news(technology)
    send_message(f"Technology\n\n{body}")
    body = summarise_news(health)
    send_message(f"Health\n\n{body}")


if __name__ == "__main__":
    main()
