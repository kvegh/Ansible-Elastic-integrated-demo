# CaC-to-AAP deployment contract

Status: inspected proposal, not a completed import or restoration test. This
contract does not select RPM/container installation, network exposure,
certificate ownership or an Elastic-to-AAP event transport.

## Reuse the existing importer

Use AutoDeploy `deploy-cac-project.yml` with its existing metadata/resource
schema and `infra.aap_configuration` 4.10.0/native Controller modules. Do not
build a second importer. Earlier bounded research established no certified
Elastic installer; it did not establish universal absence. AAP configuration
reuse is independent of the eventual Elastic installation method.

Inspected current shared source: `f6ecd8e8fc55eb79c274e9caabde3767d6044b3b`,
verified by SSH remote readback on 2026-11-15. The relevant importer/resource
files are unchanged from inspected checkout
`cf550e617439a13a50ca7da62bdf53adede39a82`. Review-policy source:
`e45b49b0de5231fbb580d828f2247161a7787863`.

The exact user-selected project ID is `Ansible-Elastic-integrated-demo`.
Once reviewed and registered, the current derivation gives the protected HTTPS
owner namespace plus `/Ansible-Elastic-integrated-demo-secrets.git`, and capture
`vaults/cac/Ansible-Elastic-integrated-demo-cac-vault.yml`. The importer template
fixes `aap_cac_project_id` to that exact ID. Do not silently lowercase it or pass
repository/file overrides.

## Required additive shared changes

Current source deliberately rejects the new ID. Before claiming shared import:

1. Add its exact spelling to `filter_plugins/cac_import.py:PROJECT_IDS` and an
   exact-case test; retain unknown-ID, traversal, HTTPS and variable-root guards.
2. For catalog/selector exposure, add `vars/use-case-catalog.yml` and an exact
   reviewed display case in `filter_plugins/use_case_setup.py:project_display_name`.
   The latter currently permits lowercase IDs and one separate RHEL exception.
   Deliberately register the associated umbrella module; do not invent a
   submodule or weaken equality checks to make selection pass.
3. Add its independently named Git-read/Vault pair in protected AutoDeploy CaC.
   Fresh-platform bootstrap also needs optional name/pair handling in
   `tasks/bootstrap-credentials.yml`, examples and tests. Its current fixed map
   does not recognize a new optional key.
4. Capture **Deploy Ansible Elastic Integrated Demo CaC** in the existing
   AutoDeploy configuration owner, referencing the shared importer Project,
   fixed project ID, project-specific Git/Vault credentials and the existing
   selected-instance token-store/trust path.

These changes are not implemented by this document. Rebase any patch on then-
current source, preserve other work, update version/docs/history, and qualify
its affected contracts before publication.

## Bootstrap, import and execution are separate

The first maintenance entrypoint is `playbooks/grow_vm_disk.yml`. Its native
Controller definition is an application Job Template, not the CaC importer.
Represent its Project, template, label and protected bindings in the private
companion first, together with the owning AutoDeploy bootstrap definition.
Parent may then create only those reviewed native definitions through supported
AAP interfaces, sync/verify exact public source, and separately launch the
user-authorized maintenance job. This introduces no temporary second importer.

That initial bootstrap does not prove ordinary shared import support. Normal
shared import still requires registration above plus actual import/readback and
repeat-apply acceptance.

For maintenance, reuse the existing hypervisor Machine credential, runtime
Vault credential and VM-only encrypted-file credential. Its existing type
injects `generic_linux_vm_config_file`, whose file holds the protected
provisioning mapping. The final maintenance contract separately binds the exact
current guest provenance and resize request; never substitute another guest's
identity or stale source-image defaults.

Do not attach a hypervisor Machine to this project's generic CaC importer: it
is API-only. The existing selector permits a route Machine only for its reviewed
Orchestrator importer. Maintenance and deployment templates have their own
independently reviewed execution credentials.

## Resource and credential boundaries

The [shape example](../examples/cac-contract.yml.example) is intentionally not
import-ready: readiness is false and review items remain. Populate and encrypt
the complete capture in the private companion. Vault passwords remain outside
both repositories; this example selects no credential source.

Initial maintenance owns one public SCM Project, one label, one template and
its VM-file credential definition. Resolve existing organization, inventory,
shared EE, credential type, Machine and runtime Vault by verified names. Do not
re-create shared objects. Pin the source revision; `main` is not a tested release.

After installation/access choices are answered, add the actual deployment and
functional-test templates plus their scoped inventory/host/group and runtime
credential definitions to the same capture. A native credential has `name`,
`organization`, `credential_type`, `inputs`; any Machine `username` belongs only
inside protected inputs. Do not invent guest accounts or edit shared credentials.

Metadata has exactly `schema_version`, `project_id`, `required_template_label`,
`resource_variables`, `checks`, `capabilities`. Map owned resource lists only.
Basic Controller deployment needs no lifecycle capability: `capabilities: {}`.
Do not request EDA access, service users or public-trust lifecycle merely because
the schema supports them. The eventual event-to-AAP path remains a separate
pending design choice.

## Runtime and acceptance

Reuse the qualified shared EE where its installed content supports the final
playbooks. The importer resolves receiver-owned `ee-proj-aap-cac` and validates
its immutable local-Hub image/verified registry credential. Inspect actual
core/Python/collections/digest; an EE name or old documentation version is not
runtime proof. No new EE, downgrade or dependency framework is selected here.

Before calling this project CaCable, demonstrate shared import, repeat apply,
and readback of exact source/target resources while preserving unrelated
objects. Imports must execute no workload, create no schedule, delete nothing
and leave new EDA definitions disabled. Run authorized deployment and maintained
functional tests separately; verify actual ingestion/search, UI, Fleet/APM and
selected integration outcomes. Source sync/import alone proves none of these.

The local AAP 2.7 Develop guide, printed pages 43–50, supplies the relevant SCM
→ Project → Job Template → execution sequence. This existing importer adds its
protected repository/instance/resource guards. Full native schema/runtime
qualification, new-project import/repeat apply and Elastic functional acceptance
remain unperformed at this contract stage.
