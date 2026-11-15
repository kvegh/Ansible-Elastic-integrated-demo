# Native Fleet, Agent and APM role

`playbooks/roles/elastic_fleet` configures one Fleet-managed native Elastic Agent
on the same RHEL 9 VM as Elasticsearch and Kibana. The servers flavor runs Fleet
Server and APM Server, together with lightweight system collection. Fleet and
APM bind only the supplied internal VM address on ports 8220 and 8200. This role
adds no public hostname, reverse proxy, firewall package, log processor, sample
application, endpoint protection or external credential store.

## Required protected contract

The parent deployment must run `elastic_core` first, with working Elasticsearch
and Kibana, the signed Elastic RPM repository and the private-CA backend pair.
It then includes this role on the same VM with privilege escalation. The role
protects all task output with `no_log: true`; the caller must also protect play
output and diffs. Check mode deliberately fails before bootstrap.

Supply these keys in the caller's protected `elastic_demo` mapping:

| Key | Meaning |
| --- | --- |
| `stack_version` | Exact shared `9.5.6` pin for Elasticsearch, Kibana and Agent |
| `bind_address` | Approved internal IPv4 VM address; never a wildcard |
| `elasticsearch_url`, `kibana_url` | Existing private HTTPS APIs secured by the core CA |
| `fleet_url` | `https://<internal-VM-address>:8220` |
| `apm_url` | `https://<internal-VM-address>:8200` |
| `operator_username`, `operator_password` | Protected bootstrap operator with Fleet/Integrations administration and service-account management privileges |
| `apm_secret_token` | Durable caller-provided secret for authenticated APM intake |

`elastic_core_result` must provide the matching `elasticsearch_url`,
`kibana_url`, `tls_ca_pem`, `tls_ca_path`, `tls_certificate_path`, and
`tls_key_path`. Files are on the managed VM. The root Agent service reads the
core's existing backend pair; it receives neither a CA private key nor a new
certificate authority. The certificate must cover the internal VM address.
No Vault credential source or sibling repository path is selected by this role.

Role defaults define generic demo-owned resource IDs, namespace and local state
paths. The same reserved IDs must remain dedicated to this project. Existing
resources with another name or preconfigured ownership are refused. Only the
explicitly managed fields are compared and updated; unrelated Fleet resources
and global defaults are preserved. Integration inputs use the documented object
form, avoiding the deprecated array input format and `policy_id` field.

## Versions and package sources

The Agent RPM is installed through `ansible.builtin.dnf` with GPG verification,
`enablerepo: elastic-demo-9` and `ELASTIC_AGENT_FLAVOR=servers`. Core leaves this
vendor repository disabled globally; the Agent transaction enables it explicitly. The ordinary flavor does not include Fleet
Server or APM Server in Elastic 9.x. RPM upgrades remain the operating system
package manager's responsibility; this role supports the exact initial demo
release rather than silently allowing version drift or Fleet binary upgrades.

Compatible stable packages were checked against the official Elastic Package
Registry for Kibana 9.5.6 on 2026-11-15: `fleet_server` 1.6.1 and `system` 3.5.0.
APM uses the 9.5.6 stack-aligned bundle shipped in the pinned Kibana release.
The exact Kibana tag's `fleet_packages.json` marks APM `forceAlignStackVersion`;
a public-registry search returning no compatible APM package does not mean that
the bundled integration is absent. No `latest`, preview package selection,
workstation installation or downloaded project helper is used at deployment.
Kibana still needs its existing outbound registry access for the System package.

## Bootstrap and recovery

The role creates a dedicated output and Fleet host, one Agent policy, and three
integration policies with fixed project IDs. These configure Fleet Server,
authenticated TLS APM intake with anonymous/RUM intake disabled, and System
collection from the existing `/var/log/messages*` and `/var/log/secure*` files.
The verified VM already runs rsyslog. CPU, memory and load are collected every
30 seconds, uptime every 60 seconds; process, per-core, disk and other unused
metrics are disabled. Windows/journald inputs are disabled.

A named `elastic/fleet-server` service token is created only when neither its
Elasticsearch credential name nor local token file exists. Its value is stored
only in a root-owned 0600 file inside a 0700 directory on this VM. Enrollment
passes that file path to the native Agent CLI, keeping the token out of process
arguments. It never force-enrolls, automatically retries token creation, deletes
credentials, or rotates tokens as a recovery shortcut.

Before enrollment the role writes a root-only intent record. The encrypted
native enrollment and that record must agree on later runs. If a response is
lost, local enrollment is absent, or token/file state disagrees, the role fails
and requires inspection of the original native outcome. Do not delete its
record, retry an uncertain create, or force enrollment to make a rerun pass.
If the intent and encrypted native enrollment both exist, starting the service
and querying its native status establishes the actual Agent ID; the matching
Fleet policy and reported healthy components must then be verified. A completed
record also prevents accepting a silently replaced Agent. Certificate, address
or version changes require an explicit maintenance plan rather than replacement.

The role invokes Fleet's documented idempotent setup endpoint; that POST does
not report a change because the API exposes no per-resource change result.
Package installs and resource creates/updates report changes. Read-before-write
comparison avoids revising unchanged owned policies. The first and second real
AAP deployment runs must still verify idempotency; it has not been demonstrated
by source inspection or syntax checks.

## Functional-test handoff

`elastic_fleet_result` is a protected host fact, not a token-bearing AAP artifact.
It contains the actual local Agent ID, Agent policy ID, all three integration
policy IDs, private Fleet/APM URLs, public CA and complete verification entries:

| Kind | Dataset | Index pattern |
| --- | --- | --- |
| logs | `system.syslog` | `logs-system.syslog-*` |
| metrics | `system.cpu` | `metrics-system.cpu-*` |
| security | `system.auth` | `logs-system.auth-*` |

The parent captures this mapping only through the existing protected mechanism
and whole-file Vault companion. Merge its `expected_agent_ids`,
`fleet_server_agent_id`, `telemetry_checks` and `tls_ca_pem` into the functional
runner's protected mapping alongside the existing URL/operator/APM inputs.
Do not commit runtime facts or decrypted output to the public repository.

Run the existing [functional verification](functional-verification.md) after
installation. Native service health alone does not prove data ingestion. Its
five-minute telemetry checks require actual recent system and authentication
activity; an idle host may have no recent authentication record and must not
silently pass. APM intake/search is tested independently of application
instrumentation. Linux authentication logs supply security-relevant data; no
endpoint prevention or detection-rule success is claimed.

## Native content and CLI selection

The bounded certified-content check did not establish qualified certified
content for this combined exact-release Fleet policy, integration, service-token
and native RPM enrollment contract. The discussed community Elastic collection's
numbered-release Elastic 9.x and selected EE qualification remain unverified.
This is a concrete coverage/qualification gap rather than a claim that no module
exists. Built-in DNF, file, systemd and assertion modules handle their supported
operations. Small `ansible.builtin.uri` tasks use the documented vendor APIs for
the remaining Fleet/service-account operations, with CA validation, no redirects
and no broad deletion.

The two native `ansible.builtin.command` calls are the supported RPM enrollment
and read-only status interfaces; Ansible's package/service modules cannot perform
enrollment or return the native Agent identity. They use argument arrays without
shell expansion. Enrollment is guarded by durable intent/native state, uses no
force option, and has no automatic retry. The status command is read-only and
bounded; its exact release's `AgentStateInfo` response defines `info.id`,
`info.version` and `info.is_managed`. No custom Python, shell installer, plugin,
module or extra framework is introduced.

Primary references checked on 2026-11-15:

- [Agent installation flavors](https://www.elastic.co/docs/reference/fleet/install-elastic-agents)
- [RPM enrollment and native status commands](https://www.elastic.co/docs/reference/fleet/agent-command-reference)
- [RPM installation layout](https://www.elastic.co/docs/reference/fleet/installation-layout)
- [Private TLS for Fleet](https://www.elastic.co/docs/reference/fleet/secure-connections)
- [Fleet setup API](https://www.elastic.co/docs/api/doc/kibana/operation/operation-post-fleet-setup)
- [Agent policy API](https://www.elastic.co/docs/api/doc/kibana/operation/operation-post-fleet-agent-policies)
- [Object-form integration policy API](https://www.elastic.co/docs/api/doc/kibana/operation/operation-post-fleet-package-policies)
- [Service-account credential listing](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-security-get-service-credentials)
- [Exact Kibana bundled-package manifest](https://github.com/elastic/kibana/blob/v9.5.6/fleet_packages.json)
- [Exact native Agent status schema](https://github.com/elastic/elastic-agent/blob/v9.5.6/pkg/control/v2/client/client.go)
- [Official package registry](https://epr.elastic.co/search?package=system&kibana.version=9.5.6)

No live Elastic installation, enrollment, idempotency run or end-to-end AAP test
has occurred for this role yet. Static validation is development evidence only;
it does not establish successful deployment or formal-review acceptance.
