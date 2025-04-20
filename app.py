from flask import Flask, render_template, request, jsonify
import openai
import os

app = Flask(__name__, template_folder='templates')

# ✅ Set your actual API key here
openai.api_key = "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"  # Replace with your OpenAI key

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
        client = openai.OpenAI(api_key=openai.api_key)  # ✅ create client with v1.0+
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # or "gpt-3.5-turbo" if not available
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        caption = response.choices[0].message.content.strip()
        return jsonify({"caption": caption})

    except Exception as e:
        print("🔥 ERROR:", e)
        return jsonify({"error": "Error generating caption. Please try again."})

if __name__ == "__main__":
    app.run(debug=True)
