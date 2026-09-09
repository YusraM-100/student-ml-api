# student-ml-api

Student roll number: `23i-0565`

FastAPI inference service used for an MLOps CI/CD exercise: feature branches →
Pull Request → GitHub Actions CI → review → merge → semantic version tag →
automated Docker build & publish to GHCR.

## Endpoints

- `GET /health` – service status and version info
- `POST /predict` – `{"value": <number>}` → `{"input": <number>, "prediction": <number>}`

## Local development

```bash
pip install -r requirements.txt
pytest -v
python app.py
```

## Docker

```bash
docker build -t student-ml-api:1.0.0 .
docker run -d --name student-ml-api -p 5000:5000 student-ml-api:1.0.0
curl http://localhost:5000/health
```
