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
