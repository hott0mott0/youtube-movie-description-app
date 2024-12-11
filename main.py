from flask import Flask, render_template, request
from markdown import markdown
from markupsafe import Markup
import youtube_transcript_api
from openai import OpenAI
import time
import os
import re

app = Flask(__name__)
index_path = "index.html"

OPENAI_API_KEY = ""
with open("openai_api_key.txt", "r") as f:
  OPENAI_API_KEY = f.read()

# OpenAI APIクライアントの初期化
client = OpenAI(api_key = OPENAI_API_KEY)


def extract_video_id(url):
    # YouTube URLからビデオIDを抽出
    video_id_match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11}).*", url)
    if video_id_match:
        return video_id_match.group(1)
    return None

def get_transcript(video_id):
    try:
        transcript = youtube_transcript_api.YouTubeTranscriptApi.get_transcript(video_id, languages=['ja'])
        return " ".join([entry['text'] for entry in transcript])
    except Exception as e:
        print(f"字幕の取得に失敗しました: {e}")
        return None

# 解説生成関数
def generate_commentary(transcript, level, content_type):
    prompt = f"以下の競馬レースの{content_type}について{level}向けに解説してください：\n\n{transcript[:4000]}"  # 文字数制限
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "あなたは将棋の専門家です。対局の様子を詳しく解説してください。"},
            {"role": "user", "content": prompt}
        ],
        max_tokens=4000
    )
    return response.choices[0].message.content

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        youtube_url = request.form.get("youtube_url")
        level = request.form.get("level")
        content_type = request.form.get("content_type")
        
        video_id = extract_video_id(youtube_url)
        if not video_id:
            return render_template(index_path, error="無効なYouTube URLです。")
        
        transcript = get_transcript(video_id)
        if not transcript:
            return render_template(index_path, error="字幕の取得に失敗しました。")
        
        explanation = markdown(generate_commentary(transcript, level, content_type))
        return render_template(index_path, explanation=Markup(explanation))
    
    return render_template(index_path)

if __name__ == "__main__":
    app.run(debug=True)
