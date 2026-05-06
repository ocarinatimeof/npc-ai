print("🔥 VERSION NUEVA ACTIVA 🔥")

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

    fallback_reply = "No estoy segura... intenta otra vez."

    # 🔴 comprobar API key
    if not API_KEY:
        print("❌ NO API KEY")
        return jsonify({"reply": fallback_reply})

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
                    {"role": "user", "content": user_message}
                ],
                "max_tokens": 60
            }
        )

        print("STATUS:", response.status_code)
        print("RAW RESPONSE:", response.text)

        # 🔴 si la API falla
        if response.status_code != 200:
            return jsonify({"reply": fallback_reply})

        result = response.json()

        # 🔴 validar respuesta
        if "choices" in result and len(result["choices"]) > 0:
            reply = result["choices"][0]["message"]["content"]
        else:
            print("❌ ERROR IA:", result)
            reply = fallback_reply

    except Exception as e:
        print("❌ EXCEPTION:", e)
        reply = fallback_reply

    return jsonify({"reply": reply})

# 🔥 necesario para Render
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
