
from flask import Flask, render_template, request, jsonify
from src.rag_chain import answer_question

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/ask", methods=["POST"])
def ask():
    data = request.get_json()

    if not data or not data.get("question", "").strip():
        return jsonify({"error": "Please enter a question."}), 400

    question = data["question"].strip()

    try:
        result = answer_question(question)
        return jsonify(result)

    except Exception as e:
        app.logger.exception("Error while answering question")
        return jsonify({"error": "Something went wrong while answering your question."}), 500


if __name__ == "__main__":
    app.run(debug=True)
