# Native Elasticsearch and Kibana core

The role configures one owned RHEL 9 x86_64 VM with the matching Elasticsearch
and Kibana 9.5.6 RPMs. The approved demo has four vCPUs, eight GiB RAM and a
twenty-GiB disk; these resource limits are a small-demo target, not a measured
vendor minimum. Elasticsearch uses a two-GiB heap and Kibana a 768-MiB Node heap.
Actual combined workload and live repeat-apply acceptance must be verified.

## Protected inputs and outputs

Supply the whole-file encrypted runtime through the deployment entrypoint.
The `elastic_demo` mapping supplies `stack_version`, assigned private
`bind_address`, `tls_dns_names`, `tls_ip_addresses`, `operator_username`
(the initial built-in administrator), `operator_password`,
`kibana_system_password`, `kibana_public_url`, and persistent
`kibana_security_encryption_key`, `kibana_saved_objects_encryption_key` and
`kibana_reporting_encryption_key`. Keep credentials and target names out of
public files. There are no default passwords or unverified TLS modes.

The protected host fact `elastic_core_result` supplies internal HTTPS URLs,
public CA PEM and root-owned original CA/certificate/key paths for the following
Fleet role. It exports no private key or password. Service-specific copies use
restricted package-user groups; the original CA key stays root-only.

## State and recovery

The role refuses unmanaged packages/data and drift in its original credential,
certificate-name, address or version binding. It records ownership before the
recoverable package steps, so an interrupted owned installation can resume
without adopting unrelated data. CA and backend ZIP members are fixed, checked
and never replaced. Existing mismatched material fails rather than being rotated.

Configure full HTTP/transport security and internal TLS explicitly; transport
binds loopback and HTTP binds the selected private interface. Security automatic
configuration is disabled only because this role supplies the complete explicit
configuration. Use the free Basic self-generated license. No extra public
service route, firewall installation or new secret store is introduced.

Seed only an absent bootstrap setting. Initial successful bootstrap authentication
is followed by explicitly persisting the administrator and Kibana service
passwords, then a private initialization marker. A completed installation does
not rotate those credentials on repeat apply. Authentication failure requires
inspection instead of an implicit reset. Handlers restart only changed service
configuration; verified HTTPS readiness is required before Fleet continues.

## Supporting tools

Built-in RPM key, repository, DNF, file, template and systemd modules cover the
host lifecycle. Bounded certified-content checks did not establish a current
qualified certified Elastic 9 installer/security bootstrap interface. The vendor
`elastic/ansible-elasticsearch` role is archived and targets versions 6/7, so it
is not selected. No community collection or new EE dependency is introduced.

The vendor certutil creates the selected PEM/SAN format. Existing Python 3's
standard ZIP library extracts only four fixed members, rejecting symlink or
changed destinations; this avoids an extra unzip package and generic extraction
paths. The small helper is used only on the owned root-only certificate workspace.
Its real output and TLS trust still require the actual AAP run to qualify.

The existing sysctl utility changes one role-owned mapping-limit file only when
the running value is insufficient; a larger existing value is retained. The
vendor keystore CLI handles its protected stdin bootstrap setting without
placing the password in command arguments. Narrow supported HTTPS APIs manage
reserved-password initialization and readiness, with the generated CA and no
redirects. These capabilities lack an established qualified certified replacement
in the selected EE. No general installer wrapper or new service is added.

## Version and platform references

Official sources checked for this implementation:

- [Elasticsearch download/version](https://www.elastic.co/downloads/elasticsearch).
- [RPM Elasticsearch installation](https://www.elastic.co/docs/deploy-manage/deploy/self-managed/install-elasticsearch-with-rpm).
- [RPM Kibana installation](https://www.elastic.co/docs/deploy-manage/deploy/self-managed/install-kibana-with-rpm).
- [Supported platform matrix](https://www.elastic.co/support/matrix/).
- [Archived vendor role](https://github.com/elastic/ansible-elasticsearch).

Offline syntax/lint and source regressions do not establish installed behavior.
The full `playbooks/deploy.yml` path must finish the internal API/telemetry and
actual nginx UI functional checks. Formal review, optional APME backends and
unselected sample-application/AAP-trigger capabilities are separate claims.

## RPM post-installation order

The exact 9.5.6 RPM post-install script invokes security auto-configuration during
DNF, before a later service template would run. Seed the supported
`xpack.security.autoconfiguration.enabled: false` setting before the initial
transaction; RPM CONFIG|NOREPLACE preserves that owned stub. Then install full
HTTP/transport TLS and protected bootstrap settings before service start.
Security remains enabled. Never remove unknown keystore entries or reset
credentials to work around this ordering. Fresh unowned config files are refused.

Exact vendor source supporting this order:

- [RPM post-install script](https://github.com/elastic/elasticsearch/blob/v9.5.6/distribution/packages/src/common/scripts/postinst).
- [AutoConfigureNode skip contract](https://github.com/elastic/elasticsearch/blob/v9.5.6/x-pack/plugin/security/cli/src/main/java/org/elasticsearch/xpack/security/cli/AutoConfigureNode.java).
- [RPM configuration preservation](https://github.com/elastic/elasticsearch/blob/v9.5.6/distribution/packages/build.gradle).
