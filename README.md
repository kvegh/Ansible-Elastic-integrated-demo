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
verification. The current deployment evidence and remaining acceptance boundary
are summarized below.

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
- `playbooks/verify.yml`: supported-interface functional checks for the public UI,
  index write/search, Fleet, APM intake/search and representative telemetry.
- `playbooks/deploy.yml`: approved single-VM RPM workflow, with explicit launch
  authorization and protected file binding. Services are deployed; full
  deployment, standalone and repeat functional acceptance passed.
- `playbooks/configure_access.yml`: one scoped nginx/DNS/Certbot UI route; shared
  nginx/auth configuration and unrelated virtual hosts are preserved.
- Core and Fleet role interfaces are documented in
  [core configuration](docs/elastic-core.md), [Fleet/APM](docs/elastic-fleet.md)
  and [UI access](docs/elastic-access.md).

[CaC contract](docs/cac-contract.md) documents integration with the existing
shared importer. Initial bootstrap and full automatic restoration must not be
claimed until tested. [Functional verification](docs/functional-verification.md)
documents the repeatable command, protected inputs and actual tested scope.

## Verified deployment — source 0.1.6

The normal deployment and standalone verification passed against implementation
`d422eadab896510b8859186a4916068fa8aca955`. Native RPM services and Fleet
enrollment are healthy. Certificate-verified public login and authenticated
Kibana access, index write/search, Fleet health, APM intake/search and recent
logs, metrics and security-relevant telemetry all passed.

The user-approved general internal HTTPS rich rule is present in running and
persistent firewall state. Independent comparison confirmed that all other
zones and existing internal rules were preserved. The matching protected
runtime values and owning-host rebuild CaC are published. The repeat apply
also passed and skipped both firewall additions. Initial shared CaC restoration
still requires the dedicated private reader's repository access.

The login check is an HTTPS GET, not browser automation. Synthetic APM intake
proves ingestion and search; instrumented application tracing and an
Elastic-to-AAP trigger remain outside the verified scope.

## Development and verification

Use existing compatible AAP execution environments and content from the approved
private automation hub. Install no workstation tools implicitly. Check current
certified content before introducing community collections or supporting code.
Keep task output protected, TLS verification enabled, changes scoped to owned
resources and tests limited to dedicated demo data.

Run the small offline regressions with the existing Ansible
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
implementation evidence. Earlier corrections cover Fleet's create-only policy
hint, pristine RPM standalone-state ownership, the System dataset name and
bounded checks against the existing proxy/certificate infrastructure. Their
versioned details remain in the decision history rather than a running README
change log.

## Supporting tools

Direct native maintenance commands and the existing hash-verified GPT/XFS helper
are justified in [implementation rationale](docs/implementation-decisions.md#disk-growth-maintenance).
The functional-check documentation explains the narrow supported-API calls.
No installer wrapper, separate service, new storage manager or testing framework
is introduced. Actual execution and full formal review remain distinct.
