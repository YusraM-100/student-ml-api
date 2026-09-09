# student-ml-api

Student Roll Number: 23i-0565

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

## Submission Evidence

- Student roll number: `23i-0565`
- Repository: https://github.com/YusraM-100/student-ml-api
- Feature PRs: [PR #1](https://github.com/YusraM-100/student-ml-api/pull/1), [PR #2](https://github.com/YusraM-100/student-ml-api/pull/2)
- Release tags: `v1.0.0`, `v1.1.0`
- `v1.1.0` merge commit: `d103069`
- Docker image: `ghcr.io/yusram-100/student-ml-api:1.1.0`
- `1.0.0` image digest: `sha256:1ae7a77015d2eb1767e238cb803fb2d53c1b04cd2fa1e0baa73c3e0db6423635`
- `1.1.0` image digest: `sha256:884436f24197efef64d98916f229d84fd9a44f20f389ae7b669dc0d83ea5271a`

The `v1.1.0` release was pulled from GHCR and verified with the health response
containing `application_version: 1.1.0` and `model_version: model-1`. Rollback
was verified by pulling `1.0.0` without rebuilding and confirming its original
health response.
