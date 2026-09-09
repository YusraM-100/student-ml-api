import json
import os

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI(title="student-ml-api")

APPLICATION_NAME = "student-ml-api"


def get_version():
    """Read the application version from the VERSION file shipped alongside app.py."""
    version_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "VERSION")
    try:
        with open(version_file) as f:
            return f.read().strip()
    except FileNotFoundError:
        return "0.0.0"


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "application": APPLICATION_NAME,
        "application_version": get_version(),
        "model_version": "model-1",
    }


@app.post("/predict")
async def predict(request: Request):
    try:
        data = await request.json()
    except (json.JSONDecodeError, UnicodeDecodeError):
        data = None

    if data is None or "value" not in data:
        return JSONResponse(
            {"error": "Missing 'value' field in request body"}, status_code=400
        )

    value = data["value"]

    if not isinstance(value, (int, float)) or isinstance(value, bool):
        return JSONResponse({"error": "'value' must be a number"}, status_code=400)

    prediction = value * 2

    return {"input": value, "prediction": prediction}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=5000)
