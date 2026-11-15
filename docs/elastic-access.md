# Kibana access through the existing proxy

The approved access stage publishes only Kibana through the existing nginx
proxy. Elasticsearch, Fleet Server and APM retain private interfaces. The
proxy connects directly to Kibana's private IPv4 on HTTPS port 5601 and verifies
its certificate against the core deployment CA with the protected internal TLS
name. No internal DNS, libvirt, firewall, shared nginx/authentication settings,
packages or ACME registration is changed.

`playbooks/configure_access.yml` can be imported after successful core and Fleet
plays in the same full AAP job. The existing dynamic `elastic_demo_guest` group
must contain exactly one guest; its `elastic_core_result.tls_ca_pem` takes
precedence. A standalone access job instead needs the durable protected CA and
existing `elastic_vm_expected.address` in that protected file (or its existing
explicit saved launch binding). It must use the same existing Machine,
runtime Vault and configuration-file credential types as the approved target.
This playbook has not been run against a live proxy; deployed access remains
unverified until normal AAP execution and actual UI functional testing pass.

## Protected input contract

The existing file credential injects `generic_linux_vm_config_file`.
`elastic_demo_config_file` may name that same credential-mounted file for the
full deployment. The file contains the existing `provisioning.hypervisor_pin`
(address, port, user, machine_id and host_keys) plus this mapping; all values
below are generic placeholders and must be sealed as whole-file Vault data:

```yaml
elastic_demo:
  access:
    enabled: true
    proxy_inventory_host: EXISTING_PROXY_INVENTORY_HOST
    machine_id: PROTECTED_PROXY_MACHINE_ID
    hostname: kibana.example.invalid
    zone: example.invalid
    record_name: kibana
    public_ipv4: PROTECTED_PROXY_PUBLIC_IPV4
    kibana_address: PROTECTED_GUEST_PRIVATE_IPV4
    kibana_tls_name: PROTECTED_INTERNAL_CERTIFICATE_NAME
    tls_ca_pem: PROTECTED_PUBLIC_CA_PEM_FOR_STANDALONE_USE
    dns_api_token: PROTECTED_EXISTING_PROVIDER_TOKEN
```

The inventory must select one existing `hypervisor`. Its address, protected
machine ID and native machine ID must agree before writes. The guest address
must match the live dynamic guest or the existing exact VM provenance. TLS
verification cannot be disabled. Neither the upstream port nor managed paths
are caller-selected: the owned paths are `/etc/nginx/conf.d/elastic-demo.conf`
and `/etc/nginx/elastic-demo-upstream-ca.pem`.

The existing shared encrypted configuration supplies the DNS zone, selected
public IPv4 and provider token. Keep those source values, target identities and
credential bindings outside public Git. The core result supplies only a public
CA, never the guest's TLS private key. The deployment does not add another
credential type or secret store.

## Reuse and capability boundaries

Existing AAP infrastructure automation requires a registered AAP instance route
and writes an AAP-specific proxy. Existing rebuild stage wrappers select their
own rebuild target and broader host/service configuration. Neither is an
Elastic access entrypoint; do not launch either with substituted Elastic inputs.

The existing shared project pins vendor roles `nginxinc.nginx` 0.26.0 and
`nginxinc.nginx_config` 0.7.1. Its wrapper also installs packages, writes common
nginx/authentication configuration and serves multiple captured services. Those
effects exceed this one-vhost stage. The cached Core 2.20.10 EE inspected for
this work has no installed `nginxinc.nginx_core` collection. A vendor namespace
or repository alone does not establish Red Hat certification or current-runtime
qualification. The small adapter uses ordinary builtin file operations and the
installed nginx parser/reload, with no role installation or shared-role copy.
The [vendor configuration role](https://github.com/nginx/ansible-role-nginx-config)
remains the existing shared-host owner; its generic capabilities are not claimed
to be absent or broken.

The existing project's documented provider gap is specific: its selected
certified content does not implement the GoDaddy exact-record-set ownership and
readback contract. The adapter therefore reuses that narrow builtin URI pattern:
fixed HTTPS provider, no redirects, one A/AAAA/CNAME name, conflicting-address
refusal and exact A readback. Existing matching records and unrelated names are
preserved. It creates only an absent selected A record.

Certificates reuse the existing production ACME account, webroot and certbot
renewal timer. The official CLI is the existing lifecycle owner; replacing it
with a general ACME module would transfer account/challenge/renewal ownership.
Only this UI certificate is requested, without registration, legal-term
acceptance or the nginx-editing plugin. The existing nginx/certbot/DNS/OpenSSL
packages, public interface, runtime and persistent HTTPS grant, ACME account and
enabled renewal timer must already be present; preflight fails otherwise.

## Scope and verification

The HTTPS virtual host does not disable inherited HTTP-level authentication or
strip Kibana's Authorization header. Only the established HTTP ACME challenge
location uses `auth_basic off`. The inspected shared main nginx template sets no
HTTP-level Basic authentication, but the actual live global configuration has
not been inspected by this worker. If existing access controls prevent the
Kibana workflow, report that constraint; do not silently bypass them.

The stage rejects unowned files and duplicate nginx hostnames, validates the
existing nginx configuration, pins SSH host keys, checks native proxy identity,
verifies private upstream TLS, waits for exact public DNS and validates nginx
before each reload. Failure restores only its own previous vhost and public CA.
An owned DNS record or issued certificate can remain after a later failure;
inspect the actual job before recovery. No unrelated resource is removed.

Only the infrastructure result is reported. An actual Kibana login/workflow,
strict external HTTPS and the existing internal Elastic functional checks remain
required after deployment; a successful nginx parser or running process is not
application acceptance. Run the complete stage without tag filtering. Check
mode is refused because certificate issuance and real endpoint verification
cannot be inferred from a dry run.

The source checks use the existing cached Core 2.20 execution image with no
network or dependency installation. Static checks do not establish that the
actual proxy already has the required packages, firewall grants or ACME state.

The checked source passed syntax validation and twelve focused Core 2.20.10
cases: file-only standalone input, live-CA precedence, refused guest/proxy/name
or tag changes, DNS ownership and alternate-route rejection, and rendered TLS
scope. Three actual builtin file-task fixtures restored existing owned bytes,
removed only newly created owned files and preserved an unrelated file. These
fixtures used temporary container files, with networking and service operations
disabled; they do not establish live proxy rollback or application acceptance.

For ordinary source syntax validation with the approved EE:

```sh
ansible-playbook --syntax-check -i /path/to/approved-inventory playbooks/configure_access.yml
```

Use the full deployment or separately selected access Job Template for actual
execution. Do not invoke the unrelated AAP instance or host rebuild stages.

## Immediate reload and rollback

The conditional HTTP-challenge reload intentionally remains a task inside the
owned-file rollback block. It must complete before certificate issuance, and
a failed reload must remain part of that same recovery path. A narrowly marked
`no-handler` lint deviation preserves this behavior; it does not suppress other
lint findings or make failures successful. Three actual built-in rollback
fixtures covered existing/new file combinations and unrelated-file preservation.
The final HTTPS reload is likewise conditional on owned configuration changes.
