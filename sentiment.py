import os
from functools import lru_cache
from transformers import pipeline

MODEL_NAME = os.getenv("SENTIMENT_MODEL", "cardiffnlp/twitter-roberta-base-sentiment-latest")

@lru_cache(maxsize=1)
def get_classifier():
    return pipeline("sentiment-analysis", model=MODEL_NAME, tokenizer=MODEL_NAME,
                    truncation=True, max_length=512)

def analyze_sentiment(text):
    result = get_classifier()(text)[0]
    label = result["label"].lower()
    if "positive" in label or label in ("label_2", "2"):
        sentiment = "positive"
    elif "negative" in label or label in ("label_0", "0"):
        sentiment = "negative"
    else:
        sentiment = "neutral"
    return {"sentiment": sentiment, "score": round(float(result["score"]) * 100, 2)}
