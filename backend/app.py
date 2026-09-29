from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route("/")
def home():
    return "Python backend is running!"


@app.route("/run", methods=["POST"])
def run():
    data = request.get_json()

    score = int(data.get("score", 0))
    time_ms = int(data.get("time", 0))
    name = data.get("name", "Unknown")
    count = int(data.get("count", 1))

    # Tady může být tvoje vlastní Python logika.
    results = []

    for i in range(count):
        results.append({
            "number": i + 1,
            "name": name if count == 1 else f"{name}{i + 1}",
            "score": score,
            "time": time_ms
        })

    return jsonify({
        "success": True,
        "results": results
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
