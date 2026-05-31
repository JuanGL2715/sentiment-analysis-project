from flask import Flask, request, render_template
from EmotionDetection.emotion_detection import emotion_detector

app = Flask("Emotion Detector")

@app.route("/emotionDetector")
def emotion_analyzer():
    text_to_analyse = request.args.get('textToAnalyze', '')
    emotion_result = emotion_detector(text_to_analyse)
    anger = emotion_result.get('anger')
    disgust = emotion_result.get('disgust')
    fear = emotion_result.get('fear')
    joy = emotion_result.get('joy')
    sadness = emotion_result.get('sadness')
    dominant_emotion = emotion_result.get('dominant_emotion')

    if not text_to_analyse.strip() or dominant_emotion is None:
        return "Invalid text! Please try again"

    response_str = (
        f"For the given statement, the system response is "
        f"'anger': {anger}, 'disgust': {disgust}, 'fear': {fear}, 'joy': {joy}, 'sadness': {sadness}. "
        f"The dominant emotion is <strong>{dominant_emotion}</strong>."
    )
    return response_str

@app.route("/")
def render_index_page():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
