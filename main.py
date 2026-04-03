from news import summarise_news, top_headlines, technology, health
from telegram import send_message

def main():
    body = summarise_news(top_headlines)
    send_message(f"Top Headlines\n\n{body}")
    body = summarise_news(technology)
    send_message(f"Technology\n\n{body}")
    body = summarise_news(health)
    send_message(f"Health\n\n{body}")

if __name__ == "__main__":
    main()