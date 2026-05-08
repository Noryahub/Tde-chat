import joblib

pipeline = joblib.load("saved_model/model.pkl")


def predict_intent(text):
    intent = pipeline.predict([text])[0]
    score = pipeline.predict_proba([text]).max()

    return intent, round(score, 3)

