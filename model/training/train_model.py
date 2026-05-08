import pandas as pd
import joblib
from sklearn.model_selection import train_test_split

from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import FunctionTransformer

from nlp.preprocess import process_nlp

df = pd.read_csv("dataset_clean.csv")
df = df.dropna(subset=["text"])
df["text"] = df["text"].astype(str)

X = df["text"]
y = df["intent"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

pipeline = Pipeline([
    ("clean", FunctionTransformer(process_nlp, validate=False)),
    ("tfidf", TfidfVectorizer(ngram_range=(1,2), lowercase=False)),
    ("clf", LogisticRegression(max_iter=1000))
])

pipeline.fit(X_train, y_train)

joblib.dump(pipeline, "model/saved_model/model.pkl")

print("modèle complet sauvegardé")