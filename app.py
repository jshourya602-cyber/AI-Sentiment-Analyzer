import os
from datetime import datetime, timezone
from dotenv import load_dotenv
from flask import Flask, flash, jsonify, redirect, render_template, request, url_for
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from sentiment import analyze_sentiment

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
if not app.secret_key:
    raise RuntimeError("SECRET_KEY is missing from .env")
client = MongoClient(os.getenv("MONGO_URI", "mongodb://localhost:27017/"), serverSelectionTimeoutMS=3000)
db = client[os.getenv("DATABASE_NAME", "sentiment_analyzer")]
reviews = db["reviews"]

def mongo_ok():
    try:
        client.admin.command("ping")
        return True
    except PyMongoError:
        return False

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    text = request.form.get("review", "").strip()
    source = request.form.get("source", "Manual")[:40]
    if not text:
        flash("Please enter some text.", "error")
        return redirect(url_for("index"))
    if len(text) > 5000:
        flash("Text must be 5,000 characters or fewer.", "error")
        return redirect(url_for("index"))
    try:
        result = analyze_sentiment(text)
    except Exception:
        app.logger.exception("Model analysis failed")
        flash("Could not load or run the sentiment model. Check setup and try again.", "error")
        return redirect(url_for("index"))
    record = {"text": text, "source": source, "sentiment": result["sentiment"],
              "score": result["score"], "created_at": datetime.now(timezone.utc)}
    try:
        reviews.insert_one(record)
        saved = True
    except PyMongoError:
        app.logger.exception("MongoDB save failed")
        saved = False
    return render_template("result.html", review=record, saved=saved)

@app.route("/dashboard")
def dashboard():
    stats = {"total": 0, "positive": 0, "negative": 0, "neutral": 0}
    records, db_ok = [], mongo_ok()
    if db_ok:
        try:
            records = list(reviews.find({}, {"text": 1, "source": 1, "sentiment": 1, "score": 1, "created_at": 1}).sort("created_at", -1).limit(100))
            stats["total"] = reviews.count_documents({})
            for label in ("positive", "negative", "neutral"):
                stats[label] = reviews.count_documents({"sentiment": label})
        except PyMongoError:
            app.logger.exception("Dashboard query failed")
            db_ok = False
    return render_template("dashboard.html", stats=stats, records=records,
                           chart_data=[stats["positive"], stats["negative"], stats["neutral"]], db_ok=db_ok)

@app.route("/health")
def health():
    return jsonify({"status": "ok", "mongodb": mongo_ok()})

if __name__ == "__main__":
    app.run(debug=os.getenv("FLASK_DEBUG", "true").lower() == "true")
