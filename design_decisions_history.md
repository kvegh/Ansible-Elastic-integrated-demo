# Design decisions history

## 2026-11-15 — Create the public implementation and private companion

- Decision: use the user-requested public Ansible-Elastic-integrated-demo
  repository and private Ansible-Elastic-integrated-demo-secrets companion.
- Authority: explicit user request to create both repositories, grow the demo
  disk and start building Ansible playbooks with CaC-to-AAP deployment. Exact
  request time is unknown; repository creation completed around 14:55 UTC.
- Outcome: both repositories were created, their visibility verified and empty
  repositories cloned over SSH. No existing repository was made public.
- Rationale: keep reusable automation public and protect all environment data
  as whole-file Vault ciphertext in the private companion. Existing Vault and
  AAP mechanisms remain outside Git; no new secret manager is introduced.
- References: implementation task bead-wd-pulk; initial source commit pending.

## 2026-11-15 — Grow only the existing demo VM to 20 GiB

- Decision: retain four vCPUs and 8 GiB RAM; grow the existing 10 GiB disk to
  20 GiB total for tiny demo data. The user explicitly approved disk, partition
  and XFS growth and this VM's shutdown/restart. Other guests are outside scope.
- Execution boundary: existing hypervisor access rules require changes through
  AAP playbooks. The approved effects do not silently waive that method boundary.
- Outcome: a narrow maintenance playbook and exact-owner preflight are being
  prepared. Growth, boot and filesystem outcomes remain unverified at entry
  creation; record actual evidence before reporting completion.
- Alternatives/tradeoff: 30 GiB would provide modest headroom, but 20 GiB is the
  accepted small-demo target. Earlier 50–100 GiB proposals were conservative
  broader-demo estimates and are not the selected target.
- References: bead-wd-cqzi; relevant implementation commit pending.

## Pending choices and implementation

Native RPM/systemd versus containers and LAN-only TLS versus an existing proxy
remain unanswered structured questions. No dependent deployment architecture is
selected. The existing CaC importer needs minimal additive project registration;
no alternate importer is selected. Elastic-to-AAP event triggering, monitored
endpoint scope and a sample instrumented application still require qualification
within the planned Basic subscription. Optional Logstash or a separate OTel
collector is not part of the selected baseline.

## 2026-11-15 16:43 UTC — Correct native tag-sequence comparison

- Initial implementation commit: e28ccdc90b43e4e2b6941f770245da0ddcbbfb97,
  version 0.0.1; public and encrypted companion baselines published and independently
  read back. Maintenance source and functional checks passed target-runtime syntax;
  functional checks also passed strict offline production lint. Live Elastic is absent.
- Actual maintenance execution stopped at its first localhost assertion before any
  managed-host change. Native cached Core 2.20 fixture confirmed that default tags
  display as a one-item sequence but direct equality against a plain list is false.
- Decision: reuse the maintained shared creator's difference-and-membership checks
  in both guards. This preserves full-run-only behavior without relying on native
  lazy sequence equality. No inventory change or security exception is needed.
- Version 0.0.2 is a focused correction within authorized maintenance scope;
  actual rerun and post-growth evidence remain pending. Fix commit ID follows.
