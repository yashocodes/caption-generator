from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__, template_folder='templates')

OPENROUTER_API_KEY = "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"  # 🔐 Replace with your actual key

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
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "deepseek/deepseek-chat-v3-0324:free",
                "messages": [
                    {"role": "user", "content": prompt}
                ]
            }
        )
        caption = response.json()["choices"][0]["message"]["content"].strip()
        return jsonify({"caption": caption})
    except Exception as e:
        return jsonify({"error": "Error generating caption. Please try again."})

if __name__ == "__main__":
    app.run(debug=True)
