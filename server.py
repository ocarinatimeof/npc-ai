print("🔥 GEMINI DEBUG 🔥")

from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)

API_KEY = os.environ.get("GEMINI_API_KEY")

@app.route("/")
def home():
    return "Servidor Gemini activo"

@app.route("/chat", methods=["POST"])
def chat():

    data = request.json
    user_message = data.get("message", "")

    print("MENSAJE:", user_message)
    print("API KEY EXISTE:", API_KEY is not None)

    if not API_KEY:
        return jsonify({"reply": "NO API KEY"})

    try:

        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"

        print("URL:", url)

        response = requests.post(
            url,
            headers={
                "Content-Type": "application/json"
            },
            json={
                "contents": [
                    {
                        "parts": [
                            {
                                "text": user_message
                            }
                        ]
                    }
                ]
            }
        )

        print("STATUS:", response.status_code)
        print("RAW RESPONSE:", response.text)

        result = response.json()

        reply = result["candidates"][0]["content"]["parts"][0]["text"]

    except Exception as e:
        print("ERROR REAL:", e)
        reply = "ERROR IA"

    return jsonify({"reply": reply})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
