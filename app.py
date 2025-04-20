from flask import Flask, render_template, request, jsonify
import openai
import os

app = Flask(__name__, template_folder='templates')

# ✅ Use environment variable for security
openai.api_key = os.getenv("OPENAI_API_KEY")

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
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        caption = response.choices[0].message.content.strip()
        return jsonify({"caption": caption})

    except Exception as e:
        print("🔥 ERROR:", e)
        return jsonify({"error": "Error generating caption. Please try again."})

if __name__ == "__main__":
    app.run(debug=True)
