import requests

DEFAULT_EMOTIONS = {
    'anger': None,
    'disgust': None,
    'fear': None,
    'joy': None,
    'sadness': None,
    'dominant_emotion': None,
}

KEYWORD_EMOTIONS = {
    'anger': ['angry', 'mad', 'furious', 'annoyed', 'irritated'],
    'joy': ['glad', 'happy', 'joyful', 'delighted', 'excited'],
    'sadness': ['sad', 'down', 'unhappy', 'depressed', 'miserable'],
    'fear': ['afraid', 'scared', 'fearful', 'terrified', 'worried'],
    'disgust': ['disgusted', 'grossed', 'nauseated', 'repulsed', 'horrified'],
}


def _local_emotion_fallback(text):
    lower_text = text.lower()
    scores = {emotion: 0.0 for emotion in KEYWORD_EMOTIONS}

    for emotion, terms in KEYWORD_EMOTIONS.items():
        for term in terms:
            if term in lower_text:
                scores[emotion] += 1.0

    if all(score == 0.0 for score in scores.values()):
        return DEFAULT_EMOTIONS.copy()

    dominant_emotion = max(scores.items(), key=lambda x: x[1])[0]
    result = DEFAULT_EMOTIONS.copy()
    result.update({emotion: (1.0 if scores[emotion] > 0.0 else 0.0) for emotion in scores})
    result['dominant_emotion'] = dominant_emotion
    return result


def emotion_detector(text_to_analyze):
    if not text_to_analyze or not isinstance(text_to_analyze, str) or not text_to_analyze.strip():
        return DEFAULT_EMOTIONS.copy()

    url = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    headers = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
    input_json = {"raw_document": {"text": text_to_analyze}}

    try:
        response = requests.post(url, json=input_json, headers=headers, timeout=10)
        response.raise_for_status()
        formatted_response = response.json()
        emotions = formatted_response.get('emotionPredictions', [])
        if not emotions or 'emotion' not in emotions[0]:
            return _local_emotion_fallback(text_to_analyze)

        emotion_scores = emotions[0]['emotion']
        if not emotion_scores:
            return _local_emotion_fallback(text_to_analyze)

        dominant_emotion = max(emotion_scores.items(), key=lambda x: x[1])[0]
        result = DEFAULT_EMOTIONS.copy()
        result.update(emotion_scores)
        result['dominant_emotion'] = dominant_emotion
        return result
    except (requests.RequestException, ValueError, KeyError, TypeError):
        return _local_emotion_fallback(text_to_analyze)