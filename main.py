import os
import requests
from openai import OpenAI

# ===== 環境変数 =====
LINE_TOKEN = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
LINE_USER_ID = os.environ["LINE_USER_ID"]
NEWS_API_KEY = os.environ["NEWS_API_KEY"]

# ===== ニュース取得 =====
url = "https://newsapi.org/v2/everything"
params = {
    "q": "artificial intelligence OR OpenAI OR AI",
    "sortBy": "publishedAt",
    "language": "en",
    "pageSize": 10,
    "apiKey": NEWS_API_KEY
}

news = requests.get(url, params=params).json()
articles = news["articles"]

text = ""
for a in articles:
    title = a["title"]
    desc = a["description"] or ""
    text += f"- {title}: {desc}\n"

# ===== ChatGPTで重要3件抽出 =====
prompt = f"""
以下はAI関連ニュースです。
重要だと思われるものを3つ選び、日本語で要約してください。

{text}
"""

client = OpenAI()

response = client.responses.create(
    model="gpt-4.1-mini",
    input=prompt
)

summary = response.output_text

# ===== LINE送信 =====
line_url = "https://api.line.me/v2/bot/message/push"
headers = {
    "Authorization": f"Bearer {LINE_TOKEN}",
    "Content-Type": "application/json"
}

data = {
    "to": LINE_USER_ID,
    "messages": [
        {"type": "text", "text": f"【本日のAIニュース】\n{summary}"}
    ]
}

requests.post(line_url, headers=headers, json=data)

print("送信完了")
