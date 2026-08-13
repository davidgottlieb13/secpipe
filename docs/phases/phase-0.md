# Phase 0 — Foundations

## Goal

Establish the base infrastructure and tooling for SecPipe: a reproducible provisioning
workflow, the first two VMs (GitLab CE + GitLab Runner), and a working CI foundation
ready to accept its first pipeline in Phase 1.

## What was built

- **Ansible control node** (`secpipe-control`): a dedicated Ubuntu Server VM acting as the
  single point of configuration management for the entire lab, communicating over SSH with
  key-based authentication.
- **Static IP addressing scheme** across a dedicated, isolated host-only virtual network
  (VMnet10), decoupling lab traffic from the host's regular network.
- **Dual-homed networking pattern**: VMs that need internet access (for package installs)
  get a second NAT-based network adapter, keeping the lab network itself fully isolated.
- **GitLab CE**, installed and configured via an idempotent Ansible role, with resource
  tuning applied to fit a 6GB RAM budget (bundled Prometheus/Grafana disabled, since a
  dedicated observability stack is planned for Phase 6; Puma/Sidekiq concurrency capped).
- **GitLab Runner**, registered against the GitLab instance using the Docker executor,
  authenticated via GitLab's current runner-authentication-token workflow (the older
  registration-token method is deprecated).

## Key decisions and trade-offs

| Decision | Reasoning |
|---|---|
| VMware Workstation native + Ansible (no Vagrant) | Avoided the paid `vagrant-vmware-desktop` plugin; kept the project fully reproducible via Ansible roles/playbooks instead |
| Dedicated Ansible control VM over WSL2 | Simpler networking (single virtual network for all lab traffic), and a more realistic "control node" pattern |
| GitLab CE bundled monitoring disabled | Redundant given the dedicated Prometheus/Grafana/Loki stack planned for Phase 6; recovers RAM for the 6GB VM budget |
| Docker executor, unprivileged for now | Principle of least privilege by default; will be revisited explicitly in Phase 2 when Docker-in-Docker builds require it |

## Challenges encountered

- **Unsupported Grafana config**: During gitlab-ctl reconfigure, GitLab failed with Mixlib::Config::UnknownConfigOptionError: Reading unsupported config value grafana. This was caused by the line grafana['enable'] = false in gitlab.rb, which is no longer recognized in recent GitLab releases. The fix was to remove that line before re-running the reconfigure.
- **Handler execution failure**: The Ansible handler designed to apply configuration (reconfigure gitlab) was triggered correctly, but it failed due to the obsolete Grafana option. This confirmed the issue was not with the handler itself, but with the configuration being applied.
- **Ruby warnings noise**: Multiple already initialized constant warnings appeared in the Ruby logs during reconfigure. While they didn’t block the installation, they made troubleshooting harder by obscuring the actual root cause.

## Result

- 3 VMs running: `secpipe-control`, `secpipe-gitlab`, `secpipe-runner`
- GitLab CE reachable and configured
- GitLab Runner online and registered, Docker executor validated with `hello-world`
- Entire setup reproducible via Ansible playbooks and roles committed to the repo

## Next: Phase 1

Write the first version of the SecPipe API (Python/FastAPI), commit it to the GitLab
repository, and write the first `.gitlab-ci.yml` — triggering our very first automated
pipeline run.
