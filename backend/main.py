import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv

from database.db import init_db, insert_analysis, search_by_term, get_all
from helper.utills import extract_top_nouns
from helper.llm import analyze_with_llm

load_dotenv()

app = Flask(__name__, static_folder="frontend", static_url_path="/")
CORS(app)

init_db()

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json(force=True)
    text = (data.get("text") or "").strip()

    if not text:
        return jsonify({"ok": False, "error": "Empty text provided"}), 400

    keywords = extract_top_nouns(text, n=3)

    try:
        llm_result = analyze_with_llm(text)
        summary = llm_result.get("summary")
        title = llm_result.get("title")
        topics = llm_result.get("topics", [])
        sentiment = llm_result.get("sentiment", "neutral")
        metadata = llm_result

        rowid = insert_analysis(text, summary, title, topics, keywords, sentiment, metadata)

        return jsonify({
            "ok": True,
            "id": rowid,
            "summary": summary,
            "title": title,
            "topics": topics,
            "keywords": keywords,
            "sentiment": sentiment,
            "metadata": metadata
        }), 200

    except Exception as e:
        return jsonify({
            "ok": False,
            "error": str(e),
            "summary": None,
            "title": None,
            "topics": [],
            "keywords": keywords,
            "sentiment": None
        }), 500


@app.route("/search", methods=["GET"])
def search():
    """Search analyses by topic or keyword."""
    topic = request.args.get("topic", "").strip()
    if not topic:
        return jsonify({"ok": False, "error": "Query param 'topic' is required"}), 400

    results = search_by_term(topic)
    return jsonify({"ok": True, "count": len(results), "results": results}), 200


@app.route("/history", methods=["GET"])
def history():
    """Return all stored analyses."""
    return jsonify({"ok": True, "results": get_all()}), 200


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_frontend(path):
    """Serve static frontend files (single-page app)."""
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    return send_from_directory(app.static_folder, "index.html")


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
