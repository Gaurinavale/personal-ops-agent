from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib

from ml_priority.dataset import TRAINING_DATA


def train():
    texts = [text for text, label in TRAINING_DATA]
    labels = [label for text, label in TRAINING_DATA]

    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(texts)

    X_train, X_test, y_train, y_test = train_test_split(
    X, labels, test_size=0.2, random_state=42, stratify=labels
)

    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    print(f"Test Accuracy: {accuracy:.2f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))
    print("Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred))

    joblib.dump(model, "ml_priority/priority_model.pkl")
    joblib.dump(vectorizer, "ml_priority/vectorizer.pkl")
    print("\nModel and vectorizer saved.")


if __name__ == "__main__":
    train()