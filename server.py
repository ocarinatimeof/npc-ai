from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# 🔑 API KEY desde Render
API_KEY = os.environ.get("OPENROUTER_API_KEY")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message", "")

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "openrouter/auto",
                "messages": [
                    {
                        "role": "system",
                        "content": "Eres un asistente útil, claro, natural y breve. No hables como un robot."
                    },
                    {
                        "role": "user",
                        "content": user_message
                    }
                ]
            }
        )

        result = response.json()

        # 🧠 respuesta IA
        reply = result["choices"][0]["message"]["content"]

    except Exception as e:
        print("ERROR:", e)
        reply = "No puedo responder ahora mismo."

    return jsonify({"reply": reply})

# 🔥 IMPORTANTE PARA RENDER
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
