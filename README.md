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

The approved installation uses native RPMs and systemd on RHEL. Pin Elasticsearch,
Kibana and Elastic Agent to 9.5.6. Bind all backend services to the existing
internal interface; publish only Kibana through the existing nginx reverse proxy,
existing Certbot account and one public DNS name. Reuse internal networking and
add scoped host entries only when required; no additional public API hostnames.

The full deployment entry point is `playbooks/deploy.yml`. It binds the existing
VM's protected SSH keys and identity, installs the core and Fleet/APM/system
telemetry, imports the single-UI access stage and finishes with actual functional
verification. The new RPM workflow is being qualified; installed functionality
must not be inferred from published or uncommitted source.

## Repository boundaries

This public repository contains reusable playbooks, generic examples, tests and
documentation. Environment-specific settings, AAP definitions, target identity,
credentials and raw evidence belong only as whole-file Ansible Vault ciphertext
in the private `Ansible-Elastic-integrated-demo-secrets` companion. Vault keys
remain outside both repositories; reuse the established protected mechanisms.

The older private Elastic-AAP-integration repository retains the verified base
VM history. It is preserved; it is not made public or silently overwritten.

## Entry points and implementation status

- `playbooks/grow_vm_disk.yml`: implemented and accepted through normal AAP
  execution. The authorized disk is now 20 GiB with grown XFS; strict independent
  native/guest checks confirm identities, partitions, source image and all other
  VM states/definitions preserved. The final run accepted the already-grown disk
  without repeating shutdown or image growth. Tested runtime source is commit
  `090e4b7189b76922a38623b388d90bfa3147afed` (0.0.4); later documentation
  revisions do not imply another workload deployment.
- `playbooks/verify.yml`: method-independent supported-interface functional checks;
  source/syntax checks do not establish deployed Elastic functionality.
- `playbooks/deploy.yml`: approved single-VM RPM workflow, with explicit launch
  authorization and protected file binding. New source remains unqualified until
  the complete AAP run and functional acceptance succeed.
- `playbooks/configure_access.yml`: one scoped nginx/DNS/Certbot UI route; shared
  nginx/auth configuration and unrelated virtual hosts are preserved.
- Core and Fleet role interfaces are documented in
  [core configuration](docs/elastic-core.md), [Fleet/APM](docs/elastic-fleet.md)
  and [UI access](docs/elastic-access.md).

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

Run the small offline maintenance regressions with the existing Ansible
execution environment (Python, PyYAML and `ansible-playbook` already included):

```sh
python3 -m unittest discover -s tests -v
```

They load actual source tasks with generic data and local execution only. They
cover full-run authorization, parsed conditional types, unchanged/missing/changed
VM states and the boundary preventing runtime metadata from replacing URLs or
credentials. They also replay the Fleet agent-policy readback contract: creation-only hints
are absent from persisted state, while drift in managed output settings must
fail. They never connect to a VM, install software or resize a disk.

The authoritative source version is in `VERSION`. See
[decision history](design_decisions_history.md) for approvals, proposals and
implementation evidence. The first RPM deployment installed the core services and exact integration
packages, then failed the Fleet policy readback assertion. Version 0.1.1 corrects
the creation-only hint comparison and reuses Fleet's existing generated server
integration, preserving enrollment and credentials. Complete deployment, UI
acceptance and repeat-run verification remain pending.

## Supporting tools

Direct native maintenance commands and the existing hash-verified GPT/XFS helper
are justified in [implementation rationale](docs/implementation-decisions.md#disk-growth-maintenance).
The functional-check documentation explains the narrow supported-API calls.
No installer wrapper, separate service, new storage manager or testing framework
is introduced. Actual execution and full formal review remain distinct.


Version 0.1.2 additionally distinguishes the RPM-started standalone Agent from
Fleet enrollment. Existing encrypted configuration alone is insufficient proof
of enrollment; pristine native state and remote ownership checks must pass before
continuing. Complete deployment and functional acceptance remain unverified.

Version 0.1.3 corrects the pinned System package process-summary dataset name.
The live third run passed prior guards and created APM before the System package
rejected the old underscore spelling. Full application acceptance remains pending.
