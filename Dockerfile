FROM python:3.11-slim

ARG APP_VERSION=unknown
ARG GIT_COMMIT=unknown
ARG BUILD_DATE=unknown

LABEL org.opencontainers.image.title="student-ml-api" \
      org.opencontainers.image.description="MLOps exercise inference API" \
      org.opencontainers.image.version="${APP_VERSION}" \
      org.opencontainers.image.revision="${GIT_COMMIT}" \
      org.opencontainers.image.created="${BUILD_DATE}" \
      org.opencontainers.image.source="https://github.com/<your-username>/student-ml-api"

WORKDIR /app

# Dependencies change far less often than application code, so they are
# copied and installed FIRST. Docker caches this layer and only re-runs
# pip install when requirements.txt itself changes (see Part 25).
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Application code changes on almost every commit - copied last so it
# never invalidates the (expensive) dependency layer above.
COPY app.py .
COPY VERSION .

EXPOSE 5000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5000"]
