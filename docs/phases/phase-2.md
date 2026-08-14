# Phase 2 — Containerization

## Goal

Package the SecPipe API as a Docker image following container security best practices,
and extend the pipeline to build and push that image automatically to a self-hosted
registry.

## What was built

- **GitLab Container Registry** enabled on `secpipe-gitlab`, running over HTTP (documented
  lab simplification — no TLS/CA available in this isolated environment).
- **Multi-stage Dockerfile**: a builder stage installs dependencies; the runtime stage
  copies only what's needed and runs the app as a dedicated non-root user (UID 1000),
  with a stdlib-only healthcheck (no extra packages installed just for that).
- **Docker-in-Docker (dind) build stage** in the pipeline: each `build_image` job gets an
  isolated, ephemeral Docker daemon as a sidecar, rather than mounting the host's Docker
  socket into the job.
- **Registry authentication** handled via GitLab's predefined CI variables
  (`CI_REGISTRY_USER`/`CI_REGISTRY_PASSWORD`) — short-lived, job-scoped credentials rather
  than a static account.
- Images tagged both with the commit's short SHA (traceability) and `latest`.

## Key decisions and trade-offs

| Decision | Reasoning |
|---|---|
| dind over Docker-socket mounting | Isolated per-job daemon avoids giving CI jobs direct control over the runner host's own Docker daemon — meaningfully safer default |
| Runner switched to `privileged = true` | Required by dind; explicitly revisited from the `privileged = false` default set in Phase 0, and documented as a deliberate, scoped trade-off rather than an oversight |
| Non-root container user | Standard container-hardening practice; limits blast radius if the running application is ever compromised |
| Plain HTTP registry, marked insecure | No TLS/CA available in an isolated home lab; explicitly flagged rather than silently ignored |
| Separate builder/runtime stages | Keeps build tooling (pip, compilers if any) out of the final shipped image, reducing its attack surface and size |

## Result

- Every push now: runs tests → builds a hardened image → pushes it to the registry with
  full traceability (SHA-tagged)
- Image verified pullable and runnable independently of the pipeline (manual pull/run test
  on the runner)

## Next: Phase 3

Shift security left into the pipeline itself: static analysis (SAST) with SonarQube,
dependency scanning (SCA), and container image scanning — including deliberately
introducing a known-vulnerable dependency to demonstrate the pipeline catching and
blocking it.
