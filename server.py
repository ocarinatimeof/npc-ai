print("🔥 VERSION TEST CHAT 🔥")

from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return "Servidor activo"

@app.route("/chat", methods=["POST"])
def chat():
    print("💬 CHAT RECIBIDO")

    data = request.json
    user_message = data.get("message", "")

    print("MENSAJE:", user_message)

    return jsonify({"reply": "respuesta test"})

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
