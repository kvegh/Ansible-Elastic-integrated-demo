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


## 2026-11-15, 19:47 UTC — Correct Fleet creation-only policy fields

- Initial RPM implementation: eb97e1c52dbae8bf81eb19c05d2a00ce64fb3008
  (0.1.0), published with paired encrypted configuration. Core services passed
  authenticated readiness and exact integration packages installed. The first
  deployment failed at 19:42:05 UTC because the playbook required a Fleet
  creation-only field in persisted readback. Complete functionality was not
  established; no successful Agent enrollment or UI route is claimed.
- Read-only API inspection confirms the owned agent policy exists with its
  ordinary desired fields, no persisted `has_fleet_server` field, and one native
  Fleet Server integration already created by that option. There are no enrolled
  Agents and no local enrollment/token markers. Exact vendor source confirms
  this convenience option is consumed during creation rather than persisted.
- Treat the hint as creation-only; compare and update only persistent desired
  fields. Validate and reuse the single native server integration under the
  exact owned policy, including its existing ID/name. Preserve fixed APM/System
  IDs, TLS checks, credentials, single-guest boundaries and strict readback.
  This routine correction avoids duplicate integrations and unnecessary removal
  or recreation of an already-created resource; it changes no architecture.
- Version 0.1.1 adds an actual-source Ansible regression for native readback and
  rejected managed-field drift. Target-runtime checks and a corrected complete
  native run remain pending at this entry. The implementation hash follows
  publication; private evidence retains the failed run and actual resource IDs.

- Subsequent validation: all eight actual-source regressions passed in cached
  Core 2.20.10/Python 3.12.15 (215.002 seconds). Strict offline production lint
  passed for application entry points and imported roles: zero failures/warnings
  across twenty files. The broader maintenance-inclusive lint additionally finds
  two pre-existing long lines in the unchanged accepted growth playbook; no new
  maintenance code is changed by this correction. Full APME scan is unavailable
  without preparing a missing managed runtime; no tool was installed.

## 2026-11-15 — Isolate the existing CaC importer source

- Actual provider answer approved a separate native source Project for the
  already-published generic importer at
  3f9788d2db2ac71522bd6b64fad213624ac9aa10 (0.64.1). Exact answer timestamp is
  not recorded here. Shared source pins remain unchanged.
- This reuses the existing importer and credential types, with one fixed-ID
  template and protected bootstrap definitions in the existing configuration
  owner. Alternative: advancing the shared Project would affect unrelated
  workstreams and was not selected. No new importer, catalog exposure, umbrella
  submodule, event transport or additional component is selected.
- Activation and complete import/repeat-readback remain pending. Public contract
  documentation now reflects this approved scope rather than earlier proposals.


## 2026-11-15 — Distinguish standalone startup from Fleet enrollment

- Fleet policy correction implementation:
  2ca4f51522696bee76fb820df7b7b84b1a2113c7 (0.1.1), published and paired with
  encrypted configuration. The corrected native run failed before reaching that
  policy stage, at 20:24:20 UTC, when the ownership guard treated encrypted Agent
  configuration existence as Fleet enrollment.
- The earlier diagnostic inspected the wrong native path and did not prove the
  actual file absent. Corrected read-only checks find a root-owned encrypted
  configuration created during the first RPM installation, no project enrollment
  or token record, and an active exact-version native Agent reporting
  `is_managed: false`. Its main configuration matches the installed RPM digest.
- Exact vendor release source confirms RPM installation starts the standalone
  Agent and standalone startup writes its identity into encrypted configuration.
  That file's existence alone does not establish Fleet enrollment. The scoped
  correction must require the pristine exact-version unmanaged state, preserve
  existing managed ownership/intent checks and verify no Fleet registration
  before first enrollment. Never delete, reset or force an unknown enrollment.
- Working 0.1.2 also folds two original maintenance YAML lines found by broader
  lint. Full parsed structure is unchanged except those strings; generic cases,
  including quoted trust paths, render both values byte-identically. This causes
  no disk growth, VM restart or maintenance job execution.
- New guard implementation, relevant tests and full live application acceptance
  remain pending here. Raw identities, digests and native results stay only in
  the encrypted companion. An unrelated GitHub repository-access action blocks
  CaC restoration; it does not authorize credential rotation or a new source.

- Main-agent direct validation passed target Core 2.20.10 syntax, assertion-type
  scan and both new regression methods (fourteen cases; 17.309 seconds) at
  21:01:57–21:02:19 UTC. Delayed delegated validation remains unconfirmed; it
  is not counted as a pass. Full lint identified decoded tab characters in the
  RPM query, so use a plain-space manifest delimiter for the fixed no-space
  configuration path and ordinary split parsing. Relevant checks are rerun for
  that narrow correction before publication; no rule suppression is introduced.

- Final corrected source passed Core 2.20.10 syntax, all assertion-type checks,
  fourteen new guard cases (19.620 seconds), and strict offline production lint
  across all twenty-seven files with zero failures/warnings. Actual execution
  was 2026-11-16 04:17:23–04:18:05 UTC; earlier submission is not execution time.
  Independent retained worker results also passed the two new methods.
  Complete application acceptance remains pending until a real deployment.


## 2026-11-16 — Match the exact System package stream contract

- Prior implementation: 192722164624476100d89ff637054b681d0b061c (0.1.2).
  Live execution passed both earlier guards, reused its Fleet Server integration
  and created the aligned APM policy. It failed System policy creation with HTTP
  400 at 04:22:47 UTC; no enrollment or UI acceptance was reached.
- Read-only server error identifies unsupported system.process_summary. Actual
  installed System 3.5.0 metadata requires system.process.summary. The complete
  thirteen-stream metric set and configured variables were checked against that
  exact contract; existing APM policy is present and System policy is absent.
- Version 0.1.3 changes that single key and adds a vendor-contract regression
  covering the complete selected stream set and minimal enabled metrics.
  No policy deletion, reset, extra component or security relaxation is selected.
  Corrected deployed acceptance remains pending; implementation hash follows.

- The exact registry archive independently confirms this as the only System/APM
  configured-field mismatch: https://epr.elastic.co/epr/system/system-3.5.0.zip.
  The focused contract regression passed in 0.012 seconds; full strict offline
  production lint passed all twenty-seven files with zero failures/warnings.


## 2026-11-16 — Reuse actual proxy prerequisites

- System correction implementation: 6c2d9b75f4cc71d451d18b0d6527a438fb0dbe71.
  Its deployment completed native software enrollment and healthy components,
  then stopped before public route changes because bind-utils is absent.
- Read-only native checks establish existing nginx/Certbot/OpenSSL, production
  account and active renewal timer. HTTPS is already accepted in runtime and
  persistent state through an unrestricted IPv4 rich rule. The shared webroot
  parent exists; Certbot temporary challenge children do not.
- Use built-in getent with service=dns, bypassing hosts-file lookup, and require
  exactly the intended IPv4 address. Recognize the existing HTTPS rich rule in
  addition to existing service/port forms, preserving runtime/persistent checks.
  Require the durable webroot parent; Certbot manages its temporary children.
- Version 0.1.4 adds actual-predicate DNS and firewall regressions. This routine
  compatibility correction installs nothing and changes no firewall policy,
  account, renewal mechanism or unrelated virtual host. Full UI/ingestion
  acceptance remains pending.

- Target Core 2.20 syntax and ten DNS/firewall predicate cases passed (12.140s).
  Full strict offline production lint passed twenty-seven files with zero
  failures/warnings at 2026-11-16 04:40:34–04:41:06 UTC. No live proxy change
  is implied by those checks; the next AAP execution establishes that outcome.


## 2026-11-16 — Terminate the verified upstream TLS probe

- Proxy compatibility implementation: 26cf75c0ec49d5f7519f3bd39efe38dcc3d5381a.
  Actual run passed existing proxy, DNS and prerequisite checks, then timed out
  waiting on the interactive OpenSSL probe. Its owned files rolled back. Native
  software repeat applied without managed-resource changes; enrollment remains
  healthy. No public UI success is claimed.
- Read-only TCP checks passed all four internal ports. Python TLS and OpenSSL
  with explicit EOF both validated the exact private chain/name in 0.02 seconds.
  Send the supported quit input and require EOF handling, retaining CA validation,
  hostname verification and failure-on-certificate-error. No insecure flag, new
  package, firewall change or service reset is introduced. Version 0.1.5 records
  that narrow correction; complete AAP/UI acceptance remains pending.
