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

    # 🔴 fallback por si todo falla
    fallback_reply = "No estoy segura... intenta otra vez."

    # 🔴 si no hay API key
    if not API_KEY:
        print("ERROR: NO API KEY")
        return jsonify({"reply": fallback_reply})

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
                        "content": """
Hablas como una persona normal en un chat.
Respondes breve, natural y sin sonar como asistente.
No das explicaciones largas.
A veces puedes ser directa o neutral.
"""
                    },
                    {
                        "role": "user",
                        "content": user_message
                    }
                ],
                "max_tokens": 60,
                "temperature": 0.8
            }
        )

        result = response.json()

        print("API RESPONSE:", result)

        # 🔴 comprobar respuesta válida
        if "choices" in result and len(result["choices"]) > 0:
            reply = result["choices"][0]["message"]["content"]
        else:
            print("ERROR IA:", result)
            reply = fallback_reply

    except Exception as e:
        print("EXCEPTION:", e)
        reply = fallback_reply

    return jsonify({"reply": reply})

# 🔥 IMPORTANTE PARA RENDER
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
