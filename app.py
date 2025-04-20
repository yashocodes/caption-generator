from flask import Flask, render_template, request, jsonify
import openai
import os
import traceback

app = Flask(__name__, template_folder='templates')

# ✅ Securely load API key from environment
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
        traceback.print_exc()
        return jsonify({"error": f"Error generating caption: {str(e)}"})

if __name__ == "__main__":
    app.run(debug=True)
