print("🔥 DEBUG TOTAL 🔥")

from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)

API_KEY = os.environ.get("OPENROUTER_API_KEY")

@app.route("/")
def home():
    return "Servidor activo"

@app.route("/chat", methods=["POST"])
def chat():
    print("---- NUEVA REQUEST ----")

    data = request.json
    print("DATA:", data)

    user_message = data.get("message", "")
    print("MENSAJE:", user_message)

    print("API_KEY EXISTE:", API_KEY is not None)

    if not API_KEY:
        print("❌ NO API KEY")
        return jsonify({"reply": "NO API KEY"})

    try:
        print("➡️ ENVIANDO A OPENROUTER")

        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "mistralai/mistral-7b-instruct:free",
                "messages": [
                    {
                        "role": "user",
                        "content": user_message
                    }
                ]
            }
        )

        print("STATUS:", response.status_code)
        print("RAW:", response.text)

        result = response.json()

        if "choices" in result:
            reply = result["choices"][0]["message"]["content"]
        else:
            reply = "ERROR RESPUESTA IA"

        return jsonify({"reply": reply})

    except Exception as e:
        print("❌ EXCEPTION:", e)
        return jsonify({"reply": "ERROR INTERNO"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
