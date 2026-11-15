# Ansible Elastic integrated demo

Ansible automation for a small Elastic Basic demo on an existing RHEL VM, with
configuration-as-code definitions for Ansible Automation Platform (AAP).

## Approved scope

The user requested Elasticsearch, Kibana, Fleet Server, Elastic Agent and APM,
plus representative logs, metrics and Security telemetry. Keep the demo small:
four vCPUs, 8 GiB RAM and a 20 GiB total disk are the current resource target.
The user explicitly approved growing only the existing demo VM disk, including
its graceful shutdown and restart. Disk growth and deployed Elastic services
must be reported separately from published source.

Native RPM/systemd versus containers and LAN-only TLS versus an existing HTTPS
proxy are pending user decisions. No installation or network choice is implied
by this initial source. Do not deploy a proposed architecture before approval.

## Repository boundaries

This public repository contains reusable playbooks, generic examples, tests and
documentation. Environment-specific settings, AAP definitions, target identity,
credentials and raw evidence belong only as whole-file Ansible Vault ciphertext
in the private `Ansible-Elastic-integrated-demo-secrets` companion. Vault keys
remain outside both repositories; reuse the established protected mechanisms.

The older private Elastic-AAP-integration repository retains the verified base
VM history. It is preserved; it is not made public or silently overwritten.

## Entry points and implementation status

- `playbooks/grow_vm_disk.yml`: implemented narrow maintenance entry point;
  exact-owner checks and explicit growth authorization are required. Its
  authorized AAP execution and independent post-growth verification are pending.
- `playbooks/verify.yml`: method-independent supported-interface functional checks;
  source/syntax checks do not establish deployed Elastic functionality.
- Elastic deployment/configuration playbooks follow the approved installation
  and TLS decisions. Elasticsearch, Kibana, Fleet/APM and data collection must
  all have explicit verification; package installation alone is insufficient.

[CaC contract](docs/cac-contract.md) documents integration with the existing
shared importer. Initial bootstrap and full automatic restoration must not be
claimed until tested. [Functional verification](docs/functional-verification.md)
documents the repeatable command, protected inputs and actual tested scope.

## Development and verification

Use existing compatible AAP execution environments and content from the approved
private automation hub. Install no workstation tools implicitly. Check current
certified content before introducing community collections or supporting code.
Keep task output protected, TLS verification enabled, changes scoped to owned
resources and tests limited to dedicated demo data.

The authoritative source version is in `VERSION`. See
[decision history](design_decisions_history.md) for approvals, proposals and
implementation evidence. This initial baseline does not claim Elastic is live.

## Supporting tools

Direct native maintenance commands and the existing hash-verified GPT/XFS helper
are justified in [implementation rationale](docs/implementation-decisions.md#disk-growth-maintenance).
The functional-check documentation explains the narrow supported-API calls.
No installer wrapper, separate service, new storage manager or testing framework
is introduced. Actual execution and full formal review remain distinct.
