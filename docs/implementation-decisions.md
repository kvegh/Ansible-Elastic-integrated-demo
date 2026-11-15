# Implementation rationale

## Disk growth maintenance

The existing VM creator is deliberately fresh-only and refuses an existing
domain/disk. Re-running it is not a resize operation. This project therefore
uses a narrow normal AAP maintenance playbook for the separately authorized
offline disk growth; its execution does not install Elastic.

Bounded certified-content assessment did not establish a suitable certified
libvirt/QCOW2 resize interface in the existing execution environment. RHEL
storage roles do not manage this hypervisor's libvirt domain and QCOW2 file
ownership. Community libvirt content would add another runtime dependency and
still require the exact-owner and existing guest-root contract. Ordinary
`ansible.builtin.command` calls to the already installed native tools are
proportionate here; this is not a new custom module or general storage manager.

The playbook binds the hypervisor, UUID, guest identity, sole owned regular disk
and public SSH keys to protected provenance. It uses argument lists for native
`virsh` and `qemu-img`, waits for graceful shutdown, grows only the offline
owned image and starts the same domain. Source-image and unrelated-VM
preservation are checked. Never shrink or substitute a disk, force another
guest off, bypass SSH host verification or blindly repeat an uncertain run.

Guest partition/filesystem expansion reuses the already deployed shared
`linux_root_growth` helper from the previously accepted generic VM deployment.
The playbook verifies its exact SHA256, root ownership and mode before running
it. That maintained helper validates a last GPT partition/direct XFS layout,
backs up the table privately and preserves partition identity while invoking
`growpart` and `xfs_growfs`. It is not copied into this project or installed
again. Other layouts, platforms, disk types and missing tooling are refused.

This small demo operation needs the existing runtime Vault, managed hypervisor
Machine access, strict two-hop SSH and installed native GPT/XFS tools. It adds
no service, store, transport or collection. Code/syntax assessment is separate
from the actual authorized AAP run and independent native/guest evidence; do
not claim a completed formal review or verified growth from source alone.

## Functional APIs

The functional checks use the supported service HTTPS APIs so they apply to
either installation method. Their detailed input, data-ownership, API-gap,
cleanup and untested-scope contract is documented in
[functional verification](functional-verification.md). They do not select a
deployment architecture or prove application instrumentation merely by sending
a synthetic APM intake request.

## Existing VM access

The approved VM already exists. Reuse its recorded machine ID, native UUID,
public SSH keys and existing managed SSH-agent proxy route; never rerun the
fresh-only VM creator. The deployment entrypoint uses ordinary built-in Ansible
file, inventory and command utilities, not a new transport or VM-management
framework. A bounded read of the machine ID and sysfs native UUID verifies the
exact guest before package changes. The private temporary trust file contains
only existing public host keys and is removed after managed-guest work.

The same credential type already used by the base workflow injects a whole-file
Runtime Vault through `generic_linux_vm_config_file`; explicit
`elastic_demo_config_file` remains supported. The deployment has its own named
credential instance, leaving the original VM-only maintenance credential intact.
All values and AAP definitions are captured in the encrypted private companion;
no sibling checkout, unencrypted inventory or new secret store is introduced.

## Fresh deployment verification metadata

A fresh install generates its internal public CA and real Fleet agent IDs on
the managed VM. The full playbook supplies these exact outputs to its final
functional stage. Only CA PEM, exact agent IDs and telemetry expectations can
be merged; service URLs, operator credentials and APM secret remain bound to
the protected file. This avoids guessed IDs and a manual edit between install
and test. Standalone verification still needs the captured protected values.
No token or private key is emitted in deployment artifacts.
