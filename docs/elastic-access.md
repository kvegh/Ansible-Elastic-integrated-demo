# Kibana access through the existing proxy

The approved access stage publishes only Kibana through the existing nginx
proxy. Elasticsearch, Fleet Server and APM retain private interfaces. The
proxy connects directly to Kibana's private IPv4 on HTTPS port 5601 and verifies
its certificate against the core deployment CA with the protected internal TLS
name. The approved internal HTTPS grant is described below; shared nginx/authentication
settings, packages and ACME registration retain their existing ownership.

`playbooks/configure_access.yml` can be imported after successful core and Fleet
plays in the same full AAP job. The existing dynamic `elastic_demo_guest` group
must contain exactly one guest; its `elastic_core_result.tls_ca_pem` takes
precedence. A standalone access job instead needs the durable protected CA and
existing `elastic_vm_expected.address` in that protected file (or its existing
explicit saved launch binding). It must use the same existing Machine,
runtime Vault and configuration-file credential types as the approved target.
The nginx and certificate stages have run successfully. Complete acceptance
previously stopped at the controller-to-proxy firewall boundary; the newly
approved internal grant still requires normal AAP application and verification.

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
    internal_firewall_zone: PROTECTED_EXISTING_INTERNAL_ZONE
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


The proxy prerequisite check uses the existing DNS-only NSS service through
`ansible.builtin.getent` (`database: ahostsv4`, `service: dns`), so local hosts
entries cannot satisfy the public-address check. No bind-utils dependency is
required. Existing runtime and persistent HTTPS acceptance can use a service,
port or unrestricted IPv4 TCP/443 rich rule; the playbook changes none of them.
Only the existing webroot parent is required because Certbot creates/removes
its challenge subdirectories. See the [built-in getent documentation](https://docs.ansible.com/projects/ansible/latest/collections/ansible/builtin/getent_module.html).

The upstream OpenSSL check uses explicit EOF handling and quit input so it
finishes after verification rather than waiting interactively. The trusted CA,
exact TLS name and verification-error failure flags remain mandatory.

## Internal HTTPS grant

The user approved general HTTPS access from the existing internal networks.
The protected `internal_firewall_zone` must match the interface carrying the
existing private proxy address and differ from the public interface's zone.
Add only the missing runtime and permanent instances of the exact rich rule
`rule service name="https" accept`. Preserve other rules, public grants, default
rejection, zone bindings and services. No firewall reload or DNS change is needed.
The grant is independent of the owned-vhost rollback and remains desired even
if a later application test fails.

The inspected existing Core 2.20 execution image has neither the certified
`redhat.rhel_system_roles` collection nor `ansible.posix` installed. Introducing
content would require a separately qualified dependency/EE change. The existing
`firewall-cmd` provides this narrow operation without installation: query both
states, add only missing rules, and read back both states. The existing host's
owning CaC uses the same additional-zone rich-rule representation, so the same
rule is captured there for a fresh rebuild. No custom helper is introduced.
