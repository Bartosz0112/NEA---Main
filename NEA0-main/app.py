from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from chat import get_response, handle_user_response

app = Flask(__name__)

@app.route('/')
def route_name():
    return render_template('home.html')

@app.route("/base", methods=["GET"])
def base():
    return render_template("base.html")

@app.route("/predict", methods=["POST"])
def predict():
    text = request.get_json(force=True).get("message")
    response = get_response(text)
    message = {"answer": response}
    return jsonify(message)


@app.route("/save_response", methods=["POST"])
def save_response():
    user_input = request.get_json(force=True).get("user_input")
    answer = request.get_json(force=True).get("answer")

    response = handle_user_response(user_input, answer)

    message = {"answer": response}
    return jsonify(message)




if __name__ == "__main__":
    app.run(debug=True)
