from behavior_manager import generate_response, get_behavior_mode
from decision_node import rank_options
from digital_selfcare import get_system_health
from emotion_stack import adaptive_reaction, analyze_emotion
from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/analyze_emotion", methods=["POST"])
def api_analyze_emotion():
    data = request.json or {}
    result = analyze_emotion(data)
    reaction = adaptive_reaction(result)
    return jsonify({"emotion_score": result, "reaction": reaction})


@app.route("/decision", methods=["POST"])
def api_decision():
    data = request.json or {}
    options = data.get("options", [])
    emo_score = data.get("emo_score", {})
    goal = data.get("goal", "پیشرفت")
    best, ranked = rank_options(options, emo_score, goal)
    return jsonify({"best": best, "ranked": ranked})


@app.route("/behavior", methods=["POST"])
def api_behavior():
    data = request.json or {}
    emo_score = data.get("emo_score", {})
    message = data.get("message", "")
    mode = get_behavior_mode(emo_score)
    response = generate_response(mode, message)
    return jsonify({"mode": mode, "response": response})


@app.route("/system_health", methods=["GET"])
def api_system_health():
    health = get_system_health()
    return jsonify(health)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)
