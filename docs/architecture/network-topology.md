# SecPipe — Network Topology

## Overview (Phase 0)

SecPipe runs entirely in VMware Workstation on a single host (24GB RAM / 8 logical processors),
using a dual-network design per VM:

- **VMnet10 (host-only, 192.168.100.0/24)** — the "lab network." All SecPipe VMs communicate
  with each other exclusively over this network. It is intentionally isolated from the host's
  home/office network.
- **VMnet8 (NAT, default VMware network)** — a secondary adapter added only to VMs that need
  outbound internet access (package installs, container image pulls). This is a deliberate
  "dual-homed" pattern: internal lab traffic and internet egress are kept on separate interfaces,
  mirroring how internal/DMZ segmentation works in real infrastructure.

## Current state (end of Phase 0)
See [`../screenshots/phase-0_architecture.png`](../screenshots/phase-0_architecture.png) for the architecture.

## Planned additions (later phases)

| VM | IP | Phase | Purpose |
|---|---|---|---|
| secpipe-k3s-server | 192.168.100.20 | 4 | Kubernetes control-plane |
| secpipe-k3s-agent | 192.168.100.21 | 4 | Kubernetes worker |
| secpipe-vault | 192.168.100.30 | 6 | Secrets management |
| secpipe-observability | 192.168.100.40 | 6 | Prometheus / Grafana / Loki |
| secpipe-sonarqube | 192.168.100.50 | 3 | SAST scanning |

## Design decisions worth noting

- **Static IPs over DHCP**: every VM has a fixed lab-network address, defined up front in a
  single addressing table. This keeps the Ansible inventory stable and every diagram/doc
  accurate without re-verification.
- **SSH key-based Ansible auth only**: no passwords are used for configuration management;
  a dedicated ed25519 keypair (`secpipe_ansible`) was generated specifically for this lab.
- **Dedicated Ansible control node instead of WSL2**: keeps all lab tooling inside the same
  isolated network as the managed nodes, avoiding Windows/WSL2 network translation quirks,
  and mirrors a realistic "bastion/control node" pattern used in real environments.

## Phase 1 update — Dual-remote Git strategy + CI pipeline

Starting in Phase 1, the repository is pushed to **two remotes**:

- **GitHub** (`origin`) — the public portfolio remote. No pipelines run here; it exists
  purely as the showcase/source-of-truth for anyone reviewing the project.
- **GitLab** (`gitlab`, self-hosted at `192.168.100.11`) — the CI/CD execution platform.
  Every push here triggers the pipeline via `secpipe-runner`.

See [`../screenshots/phase-1_architecture.png`](../screenshots/phase-1_architecture.png) for the architecture.

**Why this split**: it mirrors a real pattern some organizations use — a public/open
GitHub presence combined with an internal GitLab (or similar) instance for actual build
and deployment execution, keeping CI/CD infrastructure off the public internet while
still showcasing the code.

## Application layer (Phase 1)

The SecPipe API (Python/FastAPI, in-memory storage) was added as the payload that
travels through the pipeline in all subsequent phases: tested here, containerized in
Phase 2, scanned in Phase 3, deployed to Kubernetes in Phase 4.
