# SecPipe

A complete DevSecOps CI/CD pipeline, built from scratch in a fully self-hosted virtual lab
(VMware Workstation) — no cloud, no managed services. This project documents the process of
designing, securing, and operating a realistic CI/CD platform end to end: source control,
pipeline automation, container security scanning, Kubernetes deployment with admission
control, supply chain security, secrets management, and observability.

## Why this project

Built as a hands-on learning project and portfolio piece to develop and demonstrate practical
DevOps/DevSecOps skills, entirely in a home lab environment (24GB RAM / 8 logical processors host).

## Architecture

See [`docs/architecture/network-topology.md`](docs/architecture/network-topology.md) for the
full network diagram and design rationale.

## Progress

- [x] **Phase 0 — Foundations**: Ansible control node, GitLab CE, GitLab Runner
- [x] **Phase 1 — CI basics**: FastAPI app, first pipeline
- [ ] **Phase 2 — Containerization**: Docker build + registry push
- [ ] **Phase 3 — Shift-left security**: SAST, SCA, container image scanning
- [ ] **Phase 4 — Kubernetes**: k3s cluster, admission control (OPA/Kyverno)
- [ ] **Phase 5 — Supply chain security**: image signing (Cosign), DAST
- [ ] **Phase 6 — Secrets & observability**: Vault, Prometheus/Grafana/Loki
- [ ] **Phase 7 — Portfolio consolidation**

Detailed write-ups for each completed phase are in [`docs/phases/`](docs/phases/).

## Stack

Ansible · GitLab CE · Docker · Kubernetes (k3s) · OPA/Kyverno · Trivy/Grype · SonarQube ·
OWASP ZAP · Cosign/Sigstore · HashiCorp Vault · Prometheus · Grafana · Loki
