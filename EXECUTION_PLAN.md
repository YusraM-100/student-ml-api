# Execution Plan — student-ml-api MLOps Exercise

## What's already done for you vs. what you must do

**Done (in this package):** `app.py`, `requirements.txt`, `tests/test_app.py`,
`Dockerfile`, `.dockerignore`, `VERSION`, both workflow files, a PR template,
README, `.gitignore`, `pytest.ini`. Tests have been run and pass (4/4).

**You must do (needs your GitHub account, Docker daemon, and registry
credentials — nobody can do this from outside your machine/account):**
creating the actual repo, opening real PRs, configuring branch protection,
watching real Action runs, pushing real tags, and pulling from the real
registry. Every command below is exact — copy-paste them in order.

Replace `<username>` everywhere with your GitHub username.

---

## Phase 0 — Bootstrap the repository

```bash
mkdir student-ml-api && cd student-ml-api
git init -b main
# copy in: app.py, requirements.txt, Dockerfile, .dockerignore, VERSION,
# pytest.ini, .gitignore, README.md, tests/, .github/
git add .
git commit -m "chore: initial repository scaffold"
git remote add origin https://github.com/<username>/student-ml-api.git
git push -u origin main
```

This one commit directly on `main` is just repo initialization (empty
scaffold, no application logic) — normal practice before protection is
switched on. Everything from here on goes through a PR.

### Turn on branch protection now (Part 7)

GitHub → repo → **Settings → Branches → Add branch protection rule** →
branch name pattern `main`:

- ✅ Require a pull request before merging
- ✅ Require approvals — set to **1** if you have a collaborator/second
  account to review with; if you're solo, set to **0** but still require
  the PR itself, and note this constraint in your submission writeup
- ✅ Require status checks to pass before merging → select the `test` and
  `docker-build-check` jobs (they'll appear in this list only after the
  first CI run, so come back and tick them after Phase 1's first PR)
- ✅ Require branches to be up to date before merging
- ✅ Do not allow bypassing the above settings (include administrators)
- ❌ Do not allow force pushes / deletions on `main`

Document these exact ticked settings (with a screenshot) for your
submission — that's the "document the settings selected" requirement.

---

## Phase 1 — First feature cycle → v1.0.0

```bash
git checkout -b feature/prediction-api
# copy in app.py, requirements.txt, tests/test_app.py, Dockerfile,
# .dockerignore, VERSION, pytest.ini, .github/workflows/ci.yml
git add app.py requirements.txt pytest.ini
git commit -m "feat: add prediction endpoint and health check"
git add tests/
git commit -m "test: add API unit tests"
git add Dockerfile .dockerignore VERSION
git commit -m "build: add Dockerfile and version file"
git add .github/workflows/ci.yml .github/PULL_REQUEST_TEMPLATE.md
git commit -m "ci: add pull request validation workflow"
git push -u origin feature/prediction-api
```

Open the PR (UI, or `gh pr create --base main --title "feat: prediction API" `
`--body-file .github/PULL_REQUEST_TEMPLATE.md`). The template auto-fills
Summary/Changes/Testing Performed/Docker Impact/Checklist — fill it in
honestly before submitting.

**CI should run and pass** (`test` → `docker-build-check`). Screenshot this
as your "successful CI execution" evidence.

### Part 6 — deliberate failure (mandatory)

On the same branch:

```python
# tests/test_app.py, inside test_health
assert data["status"] == "wrong"   # was "healthy"
```

```bash
git add tests/test_app.py
git commit -m "test: temporarily break health status assertion"
git push
```

Watch the PR's CI turn red. **Screenshot the failed run** — this is your
"failed CI execution" evidence. Then fix it:

```bash
git checkout tests/test_app.py   # or manually revert the assert
git commit -am "fix: correct health endpoint test assertion"
git push
```

CI turns green again. Now merge (Part 8): use **Squash and merge** — it
keeps `main`'s history to one clean commit per feature regardless of how
many WIP/fix commits happened on the branch (including the deliberate
break-then-fix above), which matters for readable history and easy
`git log`-based traceability. A plain merge commit would work too but
would leave the intentional-failure commit visible in `main`'s history,
which is noisier for this exercise. State this choice and reasoning in
your submission.

### Tag and release v1.0.0 (Parts 13–17)

```bash
git checkout main
git pull
git tag v1.0.0
git push origin v1.0.0
```

This triggers `release.yml`. Watch it run — **screenshot the successful
release execution**. When it finishes, check
`https://github.com/<username>/student-ml-api/pkgs/container/student-ml-api`
— you should see tags `1.0.0`, `latest`, and a commit-SHA tag. Click into
the `1.0.0` tag and record its digest (`sha256:...`) for Part 16.

### Local build, run, and inspection (Parts 10–11)

```bash
docker build -t student-ml-api:1.0.0 .
docker run -d --name student-ml-api -p 5000:5000 student-ml-api:1.0.0
curl http://localhost:5000/health
curl -X POST http://localhost:5000/predict -H "Content-Type: application/json" -d '{"value": 10}'

docker images                          # note the Image ID
docker ps                              # note the Container ID
docker logs student-ml-api
docker inspect student-ml-api          # confirm exposed port, CMD, WorkingDir, and your OCI labels
docker exec -it student-ml-api sh      # poke around inside; ls /app
```

### Reproducibility proof (Part 17)

```bash
docker rm -f student-ml-api
docker rmi student-ml-api:1.0.0
docker pull ghcr.io/<username>/student-ml-api:1.0.0
docker run -d --name student-ml-api -p 5000:5000 ghcr.io/<username>/student-ml-api:1.0.0
curl http://localhost:5000/health
```
Same response, zero rebuilding — this is the point: the registry, not
the build machine, is the source of truth for what runs in production.

---

## Phase 2 — Second feature cycle → v1.1.0 (Part 18–19)

```bash
git checkout main && git pull
git checkout -b feature/model-metadata
```

Edit `app.py`'s `/health` handler to:

```python
@app.route("/health", methods=["GET"])
def health():
    return jsonify(
        {
            "status": "healthy",
            "application": APPLICATION_NAME,
            "application_version": get_version(),
            "model_version": "model-1",
        }
    ), 200
```

Update `VERSION` to `1.1.0`. Update `tests/test_app.py`'s `test_health`:

```python
def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "healthy"
    assert data["application"] == "student-ml-api"
    assert data["application_version"] == "1.1.0"
    assert data["model_version"] == "model-1"
```

```bash
git add app.py VERSION tests/test_app.py
git commit -m "feat: add model metadata to health endpoint"
git push -u origin feature/model-metadata
```

Open PR #2 with the template, let CI pass, squash-merge, then:

```bash
git checkout main && git pull
git tag v1.1.0
git push origin v1.1.0
```

Verify the registry now shows `1.0.0`, `1.1.0`, and `latest` — and that
`latest` resolves to the `1.1.0` digest (compare digests on the package
page).

---

## Phase 3 — Rollback exercise (Part 20)

Simulate a bad `1.1.0` in production:

```bash
docker rm -f student-ml-api
docker pull ghcr.io/<username>/student-ml-api:1.0.0
docker run -d --name student-ml-api -p 5000:5000 ghcr.io/<username>/student-ml-api:1.0.0
curl http://localhost:5000/health   # confirms 1.0.0 behavior is back
```

**Why this beats `git clone && pip install && python app.py`:** rollback is
a `docker pull` of an artifact that was already tested and built once —
seconds, no build step, no dependency resolution, no risk of the
environment drifting from what was actually tested. A source-based
rollback re-runs the entire build/install pipeline on the target machine,
which can fail for reasons unrelated to the code (a dependency version no
longer resolves, a system library is missing) and takes materially longer.

---

## Phase 4 — Traceability (Part 21)

Fill this in with real values from your repo for the v1.1.0 release:

```
PR:            #<number>
Merge Commit:  <sha from `git log main --oneline`>
Git Tag:       v1.1.0
Docker Image:  student-ml-api:1.1.0
Image Digest:  sha256:<from the GHCR package page>
```

You can derive the merge commit from the tag directly:
```bash
git log -1 v1.1.0
```

---

## Phase 5 — Failure analysis (Part 26, pick 2+)

**1. Application bound to 127.0.0.1**
- *Symptom:* `docker run -p 5000:5000 ...` succeeds, container shows as
  running, but `curl http://localhost:5000/health` hangs or refuses.
- *Root cause:* if `app.run(host="127.0.0.1", ...)` were used, the process
  only listens inside the container's own loopback interface, which the
  host's port mapping can't reach.
- *Evidence:* temporarily change `host="0.0.0.0"` to `host="127.0.0.1"` in
  `app.py`, rebuild, run, and capture the failed `curl`.
- *Correction:* bind to `0.0.0.0` (already done in the shipped `app.py`).

**2. Wrong container port**
- *Symptom:* `curl http://localhost:5000/health` fails even though
  `docker ps` shows the container running.
- *Root cause:* `-p` mapping doesn't match `EXPOSE`/the port Gunicorn binds
  to — e.g. running `docker run -p 8080:5000 ...` but curling `:5000`.
- *Evidence:* run with a mismatched `-p` mapping, capture the connection
  refusal, then show `docker port student-ml-api` revealing the actual
  mapping.
- *Correction:* match the host port to the container's exposed port, or
  curl the correct host port.

(Two more you could use if you want extra coverage: an invalid GHCR PAT
locally with `docker login` → auth failure; or a typo'd image tag on
`docker pull` → "manifest unknown".)

---

## Viva question answers (for your prep)

1. **Avoid pushing directly to `main`** — it bypasses review and CI, so
   broken or unvetted code can reach the branch everything else builds on.
2. **A PR is more than a merge mechanism** — it's a review checkpoint, a
   CI trigger, a documented rationale for the change, and a permanent
   record of what changed and why.
3. **CI before merge** — catches failures before they contaminate `main`,
   rather than discovering them after the fact when they're more expensive
   to isolate and fix.
4. **Image vs. container** — an image is the immutable, built artifact
   (filesystem + metadata); a container is a running (or stopped) instance
   of that image with its own writable layer and process.
5. **Why version images** — so a given deployment is traceable to an exact,
   reproducible artifact rather than "whatever `main` happened to be."
6. **Why `latest` is insufficient for production** — it's a mutable pointer
   that can silently point to a different image tomorrow; it carries no
   information about which version is actually running.
7. **Promote, don't rebuild** — rebuilding risks producing a different
   artifact (dependency drift, base image updates) than what was tested;
   promoting the exact tested artifact guarantees what you tested is what
   you ship.
8. **Purpose of a container registry** — versioned, centralized storage
   and distribution for built images, decoupling *where* an image was
   built from *where* it's run.
9. **CI vs. release workflow** — CI validates proposed changes (tests,
   build-check) before merge and never publishes; release builds and
   publishes a versioned artifact, triggered only by a version tag.
10. **Registry credentials as secrets** — hard-coding them in YAML exposes
    them to anyone with read access to the repo/history; secrets are
    encrypted and injected only at runtime.
11. **Identify the commit behind an image** — via the commit-SHA tag and/or
    the OCI `org.opencontainers.image.revision` label baked in at build
    time, checkable with `docker inspect`.
12. **Why layer ordering affects CI/CD performance** — Docker caches layers
    and invalidates everything after the first changed layer; putting
    rarely-changing steps (dependency install) before frequently-changing
    ones (app code) maximizes cache reuse and speeds up builds.
13. **Rollback 1.1.0 → 1.0.0** — `docker pull` the `1.0.0` tag from the
    registry and run it in place of `1.1.0`; no rebuild, no source checkout.
14. **Git tag vs. Docker image tag** — a Git tag marks a point in source
    history; a Docker image tag marks a specific build artifact. The
    release workflow is what links them (tag push → derives version →
    tags the image the same way).
15. **App version vs. model version changing independently** — you need
    both tracked (and reported, as `/health` now does) so you can tell
    whether a production issue came from a code change, a model change, or
    both — otherwise a bad prediction is undiagnosable from version info
    alone.

## Why not publish images from every PR (Part 22)

Every PR, including WIP and abandoned branches, would flood the registry
with unvetted, untagged-meaningfully images — burning storage, muddying
which images are trustworthy, and risking an unreviewed image accidentally
being pulled into a deployment. Publishing should happen only after code
has passed review and CI and is merged — i.e., triggered by a version tag,
not by every proposed change.
