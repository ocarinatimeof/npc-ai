print("🔥 GEMINI OFICIAL 🔥")

from flask import Flask, request, jsonify
import google.generativeai as genai
import os

app = Flask(__name__)

API_KEY = os.environ.get("GEMINI_API_KEY")

if API_KEY:
    genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("gemini-1.5-flash")

@app.route("/")
def home():
    return "Gemini funcionando"

@app.route("/chat", methods=["POST"])
def chat():

    data = request.json
    user_message = data.get("message", "")

    print("MENSAJE:", user_message)

    try:

        response = model.generate_content(
            f"""
Responde como una chica normal de Roblox.
Habla breve y natural.

Usuario: {user_message}
"""
        )

        print(response.text)

        return jsonify({
            "reply": response.text
        })

    except Exception as e:

        print("ERROR:", e)

        return jsonify({
            "reply": "ERROR IA"
        })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
