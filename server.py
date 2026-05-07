print("🔥 IA FUNCIONANDO 🔥")

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
    data = request.json
    user_message = data.get("message", "")

    if not API_KEY:
        return jsonify({"reply": "NO API KEY"})

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "meta-llama/llama-3-8b-instruct:free",
                "messages": [
                    {
                        "role": "system",
                        "content": "Responde como una chica normal de Roblox, breve y natural."
                    },
                    {
                        "role": "user",
                        "content": user_message
                    }
                ],
                "max_tokens": 60,
                "temperature": 0.9
            }
        )

        result = response.json()

        print(result)

        if "choices" in result:
            reply = result["choices"][0]["message"]["content"]
        else:
            reply = "La IA no respondió."

    except Exception as e:
        print(e)
        reply = "Error interno."

    return jsonify({"reply": reply})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
