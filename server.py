from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    mensaje = data["message"]

    respuesta = "Hola, soy un NPC 😊 Dijiste: " + mensaje

    return jsonify({"reply": respuesta})

app.run(host="0.0.0.0", port=5000)