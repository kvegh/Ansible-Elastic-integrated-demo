# Deployed functional verification

`playbooks/verify.yml` exercises deployed HTTPS interfaces from the Ansible
controller or execution environment. It selects no installation method,
network architecture, DNS name or credential store. The current source is 0.1.6;
full deployment, standalone verification and repeat functional acceptance passed.

## Current verification checkpoint

The complete deployment and standalone verification passed against source 0.1.6,
implementation `d422eadab896510b8859186a4916068fa8aca955`. Tests verified the
public certificate and Kibana login HTML, authenticated public/internal status,
index write/search and exact cleanup, Fleet health, APM intake/search and recent
logs, metrics and security telemetry from the expected Agent.

The approved general internal HTTPS grant resolved the prior controller-to-proxy
connection refusal. Its runtime and persistent presence and preservation of all
other firewall zones/rules were independently verified. The standalone run used
the persisted protected CA and Agent identity. The repeat full apply also passed; both firewall additions were skipped. Application instrumentation and an Elastic-to-AAP trigger
remain unverified, as declared below; synthetic intake is not an application demo.

## Prerequisites and inputs

Use the existing approved Ansible runtime and Vault mechanism. The controller
must be able to reach the approved nginx HTTPS listener. The approved internal
firewall grant supplies this path in the qualified deployment.
Supply an absolute regular encrypted file with an `elastic_demo` mapping,
either explicitly or through the existing credential-mounted
`generic_linux_vm_config_file` binding:

| Key | Required value |
| --- | --- |
| `elasticsearch_url`, `kibana_url`, `apm_url`, `kibana_public_url` | Selected HTTPS URLs without embedded user information, query or fragment |
| `operator_username`, `operator_password` | Protected credentials scoped to the test operations |
| `tls_ca_pem` | Trusted public CA PEM for the selected services |
| `apm_secret_token` | Separate protected APM intake bearer secret |
| `expected_agent_ids` | Nonempty list of exact Fleet agent identifiers |
| `fleet_server_agent_id` | Fleet Server agent identifier included in that list |
| `telemetry_checks` | Exactly one expectation for each `kind`: `logs`, `metrics`, `security` |

Each telemetry expectation supplies `kind`, a selected `index` pattern starting
with `logs-` or `metrics-`, an exact `dataset`, and an `agent_id` from the selected
list. Metrics use a metrics pattern; logs and security use logs patterns. Actual
configured datasets must be supplied. No target, agent or dataset is inferred.
A security-log expectation verifies selected security-relevant telemetry; it does
not prove endpoint prevention or execution of a detection rule.

The operator needs cluster monitoring, index creation/write/search/deletion for
`elastic-demo-functional-*`, read access to the selected telemetry and APM data,
and Kibana status/Fleet-agent read privileges. APM intake uses its separate
bearer token. Real targets and credentials belong only in the private encrypted
companion. The AAP job must explicitly bind the protected file;
there is no sibling-checkout fallback. No additional collection or Python module
is required by these verification playbooks.

Run the complete playbook using existing tooling:

```sh
ansible-playbook -i localhost, playbooks/verify.yml \
  --vault-password-file /protected/existing-vault-password \
  -e elastic_demo_config_file=/protected/elastic-demo.vault.yml
```

The normal AAP verification job must select the same entrypoint, protected file
and Vault binding. Do not use check mode, tags or a partial run as acceptance.
An assertion, HTTP or cleanup failure produces a failed job/nonzero exit; only
completion of every check and cleanup publishes `elastic_demo_functional` with
`passed: true`. Output is protected by default. Before writes,
`elastic_demo_functional_context` records only random nonsecret ownership IDs.
These IDs assist reconciliation if a create response is lost; never retry or
broadly delete uncertain resources blindly.

The complete deployment imports this functional stage after installation and UI
configuration. It provides only freshly generated CA PEM, exact Fleet IDs and
telemetry expectations as `elastic_demo_runtime_verification`; a strict key
allowlist retains file-bound URLs and credentials. Standalone runs use the
persisted protected values. Both the full deployment and standalone stage have now passed from the
controller using those protected inputs.

## Automated checks and test data

The test first validates the actual public UI certificate, Kibana login HTML and
authenticated supported status API through nginx, preserving inherited proxy
authentication. The login check is an HTTP GET, not browser UI automation: it
does not execute JavaScript or interact with the login form or dashboards.

After those public UI checks, it requires a responding non-red Elasticsearch cluster, available Kibana,
every selected Fleet agent active/online, and a healthy Fleet Server component.
It creates a random test-owned index, indexes a unique marker and verifies the
exact searchable document. Cleanup deletes only the exact index successfully
created by this execution. A name collision or unconfirmed creation does not
authorize deleting an existing index. The outer cleanup removes temporary public
CA trust even if a test or index-cleanup task fails.

One minimal NDJSON transaction is then posted to the APM intake API. A bounded
search must find the same trace, transaction and test-service identity in
Elasticsearch. This tiny transaction remains in the configured APM stream under
service `elastic-demo-functional` until ordinary retention removes it. The test
does not delete or reconfigure shared APM streams. That retained test record
must be in the authorized test scope before a live execution.

Finally, bounded searches require data no older than five minutes from each
selected dataset and exact agent. Logs, metrics and security are all mandatory;
empty, missing or stale data fails rather than silently skipping coverage. These
queries observe actual agent telemetry. They neither synthesize those documents
nor modify the telemetry streams.

APM intake/search does **not** establish application instrumentation. Actual
sample-application tracing, endpoint prevention/detection, and the selected
Elastic-to-AAP trigger/job outcome remain separate acceptance gaps until their
designs and test scopes are selected. The result summary explicitly marks
application instrumentation and the AAP trigger unverified. Health endpoints
alone are not treated as evidence that ingestion works.

## API selection

The bounded certified-content assessment did not establish a qualified Elastic
collection covering this combined Kibana Fleet, APM intake and Elasticsearch
verification contract in the selected AAP runtime. Numbered-release Elastic 9.x
and EE qualification of the discussed community collection remains unverified.
This is a capability/qualification gap, not a claim that no Elastic module exists.
The small `ansible.builtin.uri` tasks therefore use documented APIs, verified CA
trust, no redirects and no external helper or additional dependency.

Primary API references inspected on 2026-11-15:

- [Create an index](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-create)
- [Search](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-search)
- [Get a Fleet agent](https://www.elastic.co/docs/api/doc/kibana/v9/operation/operation-get-fleet-agents-agentid)
- [APM intake and schemas](https://www.elastic.co/docs/solutions/observability/apm/elastic-apm-events-intake-api)

These supported-interface workflows passed against the selected release. Their
scope does not establish browser-driven dashboard use, actual application
instrumentation, a full formal review or CaC restoration. Keep those remaining
gaps explicit.
