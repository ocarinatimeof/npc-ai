from flask import Flask, request, jsonify
import random

app = Flask(__name__)

# 🧠 respuestas por intención
responses = {
    "saludo": [
        "Hola...",
        "Hey.",
        "¿Qué quieres?",
        "Hmm... hola."
    ],
    "pregunta": [
        "Depende.",
        "No sabría decirte.",
        "Quizá.",
        "No estoy segura."
    ],
    "gracias": [
        "No es nada.",
        "Da igual.",
        "No hacía falta."
    ],
    "default": [
        "No sé qué decir a eso.",
        "Eso suena raro.",
        "Sigue hablando...",
        "Hmm."
    ]
}

def detectar_intencion(msg):
    msg = msg.lower()

    if any(x in msg for x in ["hola", "hey", "buenas"]):
        return "saludo"
    if "gracias" in msg:
        return "gracias"
    if "?" in msg:
        return "pregunta"
    
    return "default"

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message", "")

    intent = detectar_intencion(user_message)
    reply = random.choice(responses[intent])

    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run()
