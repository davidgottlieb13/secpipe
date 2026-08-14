# Phase 1 — CI Basics

## Goal

Ship a minimal application through SecPipe for the first time, end to end: write the app,
version it, and get GitLab CI to automatically test it on every push using the runner
built in Phase 0.

## What was built

- **SecPipe API**: a minimal FastAPI application (health check + in-memory CRUD on a
  single `items` resource), deliberately simple so the project's focus stays on the
  pipeline and security tooling rather than application complexity. A persistent
  datastore is an intentional omission at this stage.
- **Test suite**: 5 pytest tests covering the health check, item creation/retrieval,
  listing, 404 handling, and deletion.
- **Dual Git remote strategy**: GitHub as the public portfolio remote, self-hosted GitLab
  as the CI/CD execution platform — every push now goes to both.
- **First `.gitlab-ci.yml`**: a single `test` stage running the suite inside a
  `python:3.12-slim` container on `secpipe-runner`, with pip caching for faster
  subsequent runs.

## Key decisions and trade-offs

| Decision | Reasoning |
|---|---|
| In-memory storage, no database | Keeps Phase 1–2 focused on pipeline mechanics; a real datastore is a documented future extension, not a current gap |
| Vulnerable dependency deferred to Phase 3 | Preserves a clean "before/after" narrative for the SCA scanning demo, rather than baking a known CVE in from day one |
| Separate `requirements.txt` / `requirements-dev.txt` | Keeps test-only tooling (pytest, httpx) out of the eventual production container image built in Phase 2 |
| GitHub + GitLab dual remote | Public showcase decoupled from the actual CI/CD execution platform, mirroring a real enterprise pattern |

## Result

- First automated pipeline run: `pytest -v` executed by `secpipe-runner`, triggered by a
  `git push`, fully hands-off after the push.
- Application and pipeline definition both version-controlled and reproducible.

## Next: Phase 2

Containerize the SecPipe API (multi-stage Dockerfile, non-root user, minimal base image),
push the built image to GitLab's integrated container registry, and extend the pipeline
with a `build` stage.
