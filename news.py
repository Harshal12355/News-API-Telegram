import requests
import os
from dotenv import load_dotenv
from openai import OpenAI
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

asia_tokyo = ZoneInfo("UTC")

now = datetime.now(asia_tokyo)
yesterday = now - timedelta(days=1)

load_dotenv()

token = os.getenv("NEWSAPI_KEY")
openai = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai)

top_headlines_url = ('https://newsapi.org/v2/everything?'
       'q=AI&'
       f'from={yesterday.strftime("%Y-%m-%d")}&'
       'sortBy=popularity&'
       f'apiKey={token}')

technology_url = ('https://newsapi.org/v2/top-headlines?'
       'country=us&'
       'category=technology&'
       'sortBy=popularity&'
       f'apiKey={token}')

health_url = ('https://newsapi.org/v2/top-headlines?'
       'country=us&'
       'category=health&'
       'sortBy=popularity&'
       f'apiKey={token}')

top_headlines_response = requests.get(top_headlines_url).json()
technology_response = requests.get(technology_url).json()
health_response = requests.get(health_url).json()

print("Top Headlines: ", len(top_headlines_response["articles"]))
print("Technology: ", len(technology_response["articles"]))
print("Health: ", len(health_response["articles"]))

top_headlines = top_headlines_response["articles"]
technology = technology_response["articles"]
health = health_response["articles"]

def summarise_news(news):
    prompt = f"""Summarise the following news: {news}. 
    Break it down into adhd friendly format 
    and explain it like you are richard feynman.
    Rank the news by importance and relevance to the topic of AI
    Use Bullet points to list the news in order of importance.
    
    The format of the message needs to be clear and easy to read in telegram."""
    r = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1000,
    )
    return r.choices[0].message.content


print(summarise_news(top_headlines))
