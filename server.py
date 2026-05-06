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
        return jsonify({"reply": "Falta API key"})

    try:
        r = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "openrouter/auto",
                "messages": [
                    {"role": "system", "content": "Eres un asistente breve y natural."},
                    {"role": "user", "content": user_message}
                ]
            }
        )

        data = r.json()

        if "choices" not in data:
            return jsonify({"reply": "Error IA"})

        reply = data["choices"][0]["message"]["content"]

    except Exception as e:
        print(e)
        reply = "Error interno"

    return jsonify({"reply": reply})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
