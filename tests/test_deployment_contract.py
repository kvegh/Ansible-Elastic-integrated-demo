"""Offline checks for actual deployment guards and live-metadata boundaries.

Use the existing Ansible execution environment; no network or VM calls occur.
"""
import copy
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

import yaml

ROOT = Path(__file__).resolve().parents[1]


def tasks_in(value):
    if isinstance(value, dict):
        if "name" in value:
            yield value
        for item in value.values():
            yield from tasks_in(item)
    elif isinstance(value, list):
        for item in value:
            yield from tasks_in(item)


class DeploymentContractTests(unittest.TestCase):
    def task(self, filename, name):
        source = yaml.safe_load((ROOT / "playbooks" / filename).read_text())
        return copy.deepcopy(next(item for item in tasks_in(source) if item.get("name") == name))

    def run_task(self, task, variables, options=()):
        executable = shutil.which("ansible-playbook")
        self.assertIsNotNone(executable, "Use the existing Ansible execution environment")
        play = [{"hosts": "localhost", "connection": "local", "gather_facts": False,
                 "vars": variables, "tasks": [task]}]
        with tempfile.TemporaryDirectory(prefix="elastic-deploy-contract-") as folder:
            path = Path(folder) / "fixture.yml"
            path.write_text(yaml.safe_dump(play, sort_keys=False))
            return subprocess.run([executable, "-i", "localhost,hypervisor,", str(path), *options],
                                  capture_output=True, text=True, timeout=60, check=False)

    def test_all_playbook_assertions_parse_as_strings(self):
        count = 0
        for path in (ROOT / "playbooks").rglob("*.yml"):
            for task in tasks_in(yaml.safe_load(path.read_text())):
                assertion = task.get("ansible.builtin.assert")
                if not assertion:
                    continue
                conditions = assertion.get("that", [])
                conditions = conditions if isinstance(conditions, list) else [conditions]
                for condition in conditions:
                    self.assertIsInstance(condition, str, f"{path.name}: {task['name']}")
                    count += 1
        self.assertGreater(count, 0)

    def test_actual_deploy_guard_requires_authorized_complete_run(self):
        task = self.task("deploy.yml", "Require a complete explicitly authorized deployment")
        for allowed, options, expected in [(True, (), 0), (False, (), 2),
                                            (True, ("--tags", "custom"), 2),
                                            (True, ("--skip-tags", "custom"), 2)]:
            with self.subTest(allowed=allowed, options=options):
                task["tags"] = ["always"]
                result = self.run_task(task, {"elastic_demo_deploy_authorized": allowed}, options)
                self.assertEqual(result.returncode, expected, result.stdout + result.stderr)

    def test_agent_policy_readback_accepts_create_only_hint_and_rejects_drift(self):
        define = self.task("roles/elastic_fleet/tasks/main.yml", "Elastic Fleet | Define the single-host Fleet policy")
        verify = self.task("roles/elastic_fleet/tasks/resource.yml",
                           "Elastic Fleet | Require all explicitly configured fields to have survived API validation")
        # Fleet's create hint is absent from the real 9.5.6 persisted policy.
        observed = {
            "id": "demo-policy", "name": "Elastic demo single VM",
            "description": "Managed by Ansible-Elastic-integrated-demo; single-VM policy.",
            "namespace": "demo", "monitoring_enabled": ["logs", "metrics"],
            "data_output_id": "demo-output", "monitoring_output_id": "demo-output",
            "fleet_server_host_id": "demo-fleet-host", "is_default": False,
            "is_default_fleet_server": False, "revision": 1, "status": "active",
            "package_policies": [{"id": "native-fleet-policy", "name": "fleet_server-1",
                                  "package": {"name": "fleet_server", "version": "1.6.1"}}],
        }
        for drift, expected in [(False, 0), (True, 2)]:
            with self.subTest(drift=drift):
                item = copy.deepcopy(observed)
                if drift:
                    item["monitoring_output_id"] = "unexpected-output"
                variables = {
                    "elastic_fleet_agent_policy_id": "demo-policy",
                    "elastic_fleet_namespace": "demo", "elastic_fleet_output_id": "demo-output",
                    "elastic_fleet_host_id": "demo-fleet-host",
                    "__elastic_fleet_resource": "{{ __elastic_fleet_policy_resource }}",
                    "__elastic_fleet_final_resource": {"json": {"item": item}},
                }
                result = self.run_task({"name": "Replay native policy readback", "block": [define, verify]}, variables)
                self.assertEqual(result.returncode, expected, result.stdout + result.stderr)

    def test_native_fleet_child_reuse_preserves_single_parent_boundary(self):
        names = ["Identify Fleet Server integrations on the owned parent policy",
                 "Require exactly one native Fleet Server integration before reuse",
                 "Bind the one native Fleet Server integration",
                 "Validate ownership and version before changing the native integration"]
        tasks = [self.task("roles/elastic_fleet/tasks/main.yml", "Elastic Fleet | " + name) for name in names]
        child = {"id": "native-fleet-policy", "name": "fleet_server-1", "namespace": "",
                 "policy_ids": ["demo-policy"], "package": {"name": "fleet_server", "version": "1.6.1"}}
        cases = [("native", [child], 0), ("missing", [], 2),
                 ("duplicate", [child, copy.deepcopy(child)], 2)]
        for key, value in [("policy_ids", ["demo-policy", "another-policy"]),
                           ("namespace", "unrelated"), ("is_preconfigured", True)]:
            changed = copy.deepcopy(child)
            changed[key] = value
            cases.append((key, [changed], 2))
        for name, children, expected in cases:
            with self.subTest(case=name):
                variables = {"elastic_fleet_agent_policy_id": "demo-policy", "elastic_fleet_namespace": "demo",
                             "elastic_fleet_server_package_version": "1.6.1",
                             "__elastic_fleet_final_resource": {"json": {"item": {"package_policies": children}}}}
                result = self.run_task({"name": "Replay native Fleet child ownership", "block": tasks}, variables)
                self.assertEqual(result.returncode, expected, result.stdout + result.stderr)

    def test_pristine_rpm_standalone_accepts_native_identity_and_rejects_drift(self):
        filename = "roles/elastic_fleet/tasks/preflight.yml"
        names = ["Select the exact main-config RPM manifest entry",
                 "Require the pinned native RPM and one SHA256 configuration record",
                 "Require pristine unmanaged state before accepting package-created encrypted identity",
                 "Record the proven pristine standalone path for the remote identity guard",
                 "Refuse an existing enrollment without this role's ownership record"]
        tasks = [self.task(filename, "Elastic Fleet | " + name) for name in names]
        tasks.append(self.task("roles/elastic_fleet/tasks/main.yml",
                               "Elastic Fleet | Refuse to adopt a standalone identity already registered in Fleet"))
        digest = "a" * 64
        valid = {
            "elastic_demo": {"stack_version": "9.5.6"},
            "__elastic_fleet_token_stat": {"exists": False},
            "__elastic_fleet_enrollment_stat": {"exists": False},
            "__elastic_fleet_encrypted_config_stat": {"exists": True},
            "__elastic_fleet_pristine_standalone": False,
            "__elastic_fleet_main_config": {"stat": {"isreg": True, "islnk": False,
                "uid": 0, "mode": "0600", "checksum": digest}},
            "__elastic_fleet_rpm_manifest": {"stdout_lines": ["9.5.6", "8",
                "/etc/elastic-agent/elastic-agent.yml " + digest]},
            "__elastic_fleet_initial_agent_status": {"rc": 1},
            "__elastic_fleet_initial_native_status": {"info": {
                "is_managed": False, "version": "9.5.6", "id": "native-standalone-agent"}},
            "__elastic_fleet_initial_remote_registration": {"status": 404},
        }
        cases = [("pristine degraded standalone", valid, 0)]
        for name, key, value in [
                ("managed", "is_managed", True), ("wrong native version", "version", "9.5.5"),
                ("missing identity", "id", "")]:
            changed = copy.deepcopy(valid)
            changed["__elastic_fleet_initial_native_status"]["info"][key] = value
            cases.append((name, changed, 2))
        for name, key, value in [("wrong digest", "checksum", "b" * 64),
                                 ("symlink config", "islnk", True)]:
            changed = copy.deepcopy(valid)
            changed["__elastic_fleet_main_config"]["stat"][key] = value
            cases.append((name, changed, 2))
        changed = copy.deepcopy(valid)
        changed["__elastic_fleet_rpm_manifest"]["stdout_lines"][1] = "1"
        cases.append(("wrong manifest algorithm", changed, 2))
        changed = copy.deepcopy(valid)
        changed["__elastic_fleet_token_stat"]["exists"] = True
        cases.append(("partial role token", changed, 2))
        changed = copy.deepcopy(valid)
        changed["__elastic_fleet_initial_remote_registration"]["status"] = 200
        cases.append(("registered native identity", changed, 2))
        for name, variables, expected in cases:
            with self.subTest(case=name):
                result = self.run_task({"name": "Replay actual pristine native state guards", "block": tasks}, variables)
                self.assertEqual(result.returncode, expected, result.stdout + result.stderr)

    def test_owned_native_pair_preserves_immutable_intent_and_rejects_missing_records(self):
        filename = "roles/elastic_fleet/tasks/preflight.yml"
        pair = self.task(filename, "Elastic Fleet | Refuse an existing enrollment without this role's ownership record")
        immutable = self.task(filename, "Elastic Fleet | Preserve the previous enrollment instead of forcing a replacement")
        cases = [("owned paired state", True, True, "same", 0),
                 ("fresh absent state", False, False, "same", 0),
                 ("missing ownership record", True, False, "same", 2),
                 ("missing native encrypted state", False, True, "same", 2),
                 ("changed recorded intent", True, True, "different", 2)]
        for name, encrypted, recorded, previous, expected in cases:
            with self.subTest(case=name):
                variables = {
                    "__elastic_fleet_encrypted_config_stat": {"exists": encrypted},
                    "__elastic_fleet_enrollment_stat": {"exists": recorded},
                    "__elastic_fleet_pristine_standalone": False,
                    "__elastic_fleet_prior_enrollment": {"intent": {"identity": previous}},
                    "__elastic_fleet_enrollment_intent": {"identity": "same"},
                }
                result = self.run_task({"name": "Replay actual paired-state guards", "block": [pair, immutable]}, variables)
                self.assertEqual(result.returncode, expected, result.stdout + result.stderr)

    def test_system_stream_names_match_pinned_registry_contract(self):
        # System 3.5.0 metadata from the installed EPM API; process.summary uses a dot.
        task = self.task("roles/elastic_fleet/tasks/policies.yml",
                         "Elastic Fleet | Define only Fleet Server, APM intake and bounded Linux telemetry")
        resources = task["ansible.builtin.set_fact"]["__elastic_fleet_package_resources"]
        body = next(r["body"] for r in resources if r["id"] == "elastic-demo-system-integration")
        streams = body["inputs"]["system-system/metrics"]["streams"]
        datasets = {"core", "cpu", "diskio", "filesystem", "fsstat", "load", "memory",
                    "network", "ntp", "process", "process.summary", "socket_summary", "uptime"}
        self.assertEqual(set(streams), {"system." + name for name in datasets})
        self.assertEqual({name for name, config in streams.items() if config["enabled"]},
                         {"system.cpu", "system.memory", "system.load", "system.uptime"})

    def test_live_metadata_cannot_replace_urls_or_credentials(self):
        task = self.task("verify.yml", "Restrict live deployment metadata to trust and exact telemetry identity")
        for metadata, expected in [({"tls_ca_pem": "public-ca", "expected_agent_ids": ["demo-agent"]}, 0),
                                   ({"operator_password": "unapproved-override"}, 2),
                                   ({"elasticsearch_url": "https://elsewhere.example.invalid"}, 2)]:
            with self.subTest(keys=list(metadata)):
                result = self.run_task(task, {"elastic_demo_runtime_verification": metadata})
                self.assertEqual(result.returncode, expected, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
