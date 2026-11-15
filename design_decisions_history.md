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

## 2026-11-15 — Correct final verification scalar after actual disk growth

- Guard fix commit: 935a5a5e633318462ea0555d767e43e2368dbff8 (0.0.2).
  Native AAP run began 16:53:54.321223 UTC and ended 16:55:02.552767 UTC.
  Shutdown, offline resize, restart and the existing GPT/XFS helper succeeded.
  Final acceptance failed because YAML parsed an unquoted colon-space inside
  a regular expression as a mapping instead of a conditional string.
- Immediate read-only native inspection confirms the exact selected VM running
  and its disk exactly twenty GiB. No emergency restart or blind growth retry.
- Decision: express that assertion as an explicit folded string and verify every
  assert condition's parsed type. Do not enable broken conditionals or weaken
  acceptance. Version 0.0.3 is a focused correction; the existing twenty-GiB
  branch skips shutdown and image growth on the authorized verification rerun.
- Source checks and actual next-job/post-proof outcomes remain distinct. Fix
  commit ID and final evidence follow after execution; no live Elastic claim.

## 2026-11-15 — Correct state parsing using actual native evidence

- Scalar fix commit: 9816bac934502069f73b8fe748385ef5ce735aed (0.0.3).
  Its verification rerun skipped all six shutdown/image-growth tasks and
  failed the nonempty parsed-state assertion; no repeated resize occurred.
- Independent strict native/guest checks at 17:05:33.910601–17:05:37.832923 UTC
  confirm twenty-GiB disk, grown XFS, preserved guest/native/GPT/filesystem
  identities, all thirteen VM states/definitions and the original image hash.
- Actual native output replayed through the exact source parser in cached
  Core 2.20 reproduced zero parsed rows; ordinary Python parsing found thirteen.
  This confirmed template backslash escaping, rather than physical preservation.
- Decision: use an anchored, non-greedy expression without backslash escaping,
  preserving the exact nonempty row-count and paired identity/state checks.
  Actual-output positive replay parses thirteen rows. Negative cases and the
  final corrected AAP run must pass before claiming playbook acceptance.
- Version 0.0.4 remains a narrow compatibility correction. No broken-condition
  setting, reduced verification, new dependency or access exception is selected.
  Implementation commit and final execution proof follow after publication.

## 2026-11-15 — Maintenance acceptance and paired CaC evidence

- Implementation commit: 090e4b7189b76922a38623b388d90bfa3147afed
  (0.0.4), published and independently SSH-readback verified. Three maintained
  regressions passed in cached Core 2.20 in 5.971 seconds, covering actual source
  tag guards, all assertion types and native-output parser-to-assertion flow.
  The corrected source also passed target-runtime syntax.
- Normal AAP final acceptance succeeded 17:15:21.220180–17:15:58.799007 UTC
  (37.579 seconds): no failures or unreachable hosts, all six offline growth
  steps skipped on the already-grown image, root helper reports no further
  change, all final capacity/identity/state/source checks accepted.
- Earlier failures remain documented; this is corrected eventual acceptance,
  not a first-pass failure-free deployment. Independent native/guest diagnosis
  had already confirmed disk/XFS/GPT/identity and all thirteen definitions/states
  against the original protected baseline. Final independent post-proof follows
  the successful run and remains only in the encrypted companion.
- The user reiterated keeping public playbooks paired with private CaC values.
  Preserve the tested immutable public source pin, saved authorization=false,
  actual object bindings, original ten-GiB creation history and separate growth/
  acceptance evidence in whole-file Vault. Do not alter the old base artifacts.
- Version 0.0.5 documents acceptance; the AAP runtime remains pinned to the tested
  0.0.4 implementation. Full shared import/repeat restoration and live Elastic
  functionality remain unverified; installation and TLS choices remain pending.

## 2026-11-15 — Approve native RPMs and one public UI route

- Actual user answers resolve the earlier questions: native RPM/systemd; the
  existing nginx reverse proxy with a new virtual host, existing Certbot SSL and
  public DNS for only the Kibana UI. Elasticsearch, Fleet and APM stay internal.
  The user reiterated internal interfaces wherever possible and permits scoped
  host entries or existing libvirt resolution when necessary. Exact answer
  timestamps are unavailable; implementation subtasks were created 18:13 UTC.
- Alternative: four public HTTPS service names was explained and not selected.
  Do not ask the resolved installation/exposure questions again or add those
  routes. No additional VM or optional Logstash/OTel component is selected.
- Match the official Elastic 9.5.6 RPM set on the existing supported RHEL 9 VM,
  with modest component memory limits for the accepted eight-GiB demo. Generate
  durable strong application secrets once in the established Runtime Vault; use
  the existing credential type with a distinct application credential instance.
- Preserve the original maintenance input and creation/growth history. The new
  workflow uses strict existing-guest identity, core/Fleet roles, one scoped UI
  adapter and same-job functional tests. Protected values remain whole-file
  Vault and native AAP definitions remain paired with source pins.
- Version 0.1.0 is the new implementation candidate. Syntax/lint/source checks
  and live complete AAP acceptance remain separate, and are pending here.
  Sample application instrumentation, endpoint prevention and a licensed or
  Basic-compatible event-to-AAP design remain explicitly unselected details.
