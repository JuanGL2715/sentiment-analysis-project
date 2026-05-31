from flask import Flask, request
from SentimentAnalysis import sentiment_analyzer

app = Flask(__name__)

@app.route("/sentimentAnalyzer")
def analyze_sentiment():

    text_to_analyze = request.args.get(
        "textToAnalyze"
    )

    response = sentiment_analyzer(
        text_to_analyze
    )

    return str(response)

@app.route("/")
def home():
    return "Sentiment Analyzer Running"

app.run(
    host="0.0.0.0",
    port=5000
)