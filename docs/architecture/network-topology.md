# SecPipe — Network Topology (Phase 0)

## Overview

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
