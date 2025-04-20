from flask import Flask, render_template, request, jsonify
import requests
import os
import traceback

app = Flask(__name__, template_folder='templates')

# ✅ Use your OpenRouter API key (get from https://openrouter.ai)
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    topic = request.form.get("topic")
    emotion = request.form.get("emotion")
    platform = request.form.get("platform")

    prompt = f"""
Generate 1 short caption for {platform}.
Topic: {topic}
Tone: {emotion}
Rules: under 30 words, 1–2 emojis, 1–2 hashtags, no explanation, no formatting, return plain caption only.
"""

    try:
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://yourdomain.com",  # Optional: update with your actual site
            "X-Title": "Caption Generator"
        }

        data = {
            "model": "deepseek/deepseek-chat-v3-0324:free",
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }

        response = requests.post("https://openrouter.ai/api/v1/chat/completions", json=data, headers=headers)
        result = response.json()

        caption = result["choices"][0]["message"]["content"].strip()
        return jsonify({"caption": caption})

    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": f"Error generating caption: {str(e)}"})

if __name__ == "__main__":
    app.run(debug=True)
