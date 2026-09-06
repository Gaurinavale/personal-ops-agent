import joblib
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Personal Ops - Priority Predictor")

# Load the trained model and vectorizer ONCE when the server starts
model = joblib.load("ml_priority/priority_model.pkl")
vectorizer = joblib.load("ml_priority/vectorizer.pkl")


@mcp.tool()
def predict_priority(task_title: str) -> dict:
    """
    Predict the priority (high, medium, or low) of a task based on its title,
    using a custom-trained TF-IDF + Logistic Regression model.

    Args:
        task_title: The text of the task to classify.
    """
    # Transform the input text using the SAME vectorizer used during training
    features = vectorizer.transform([task_title])

    # Predict the priority label
    prediction = model.predict(features)[0]

    # Get confidence score for the predicted class
    probabilities = model.predict_proba(features)[0]
    confidence = max(probabilities)

    return {
        "task_title": task_title,
        "predicted_priority": prediction,
        "confidence": round(float(confidence), 2),
    }