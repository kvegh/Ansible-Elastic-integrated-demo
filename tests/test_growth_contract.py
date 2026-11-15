"""Offline regression for actual growth guards, state parser and assertions.

Run with the existing execution environment's Python and ansible-playbook:
    python3 -m unittest discover -s tests -p test_growth_contract.py -v
No VM connection, network, collection download or package installation occurs.
"""
import copy
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

import yaml

SOURCE = Path(__file__).resolve().parents[1] / "playbooks/grow_vm_disk.yml"


def tasks_in(value):
    if isinstance(value, dict):
        if "name" in value:
            yield value
        for nested in value.values():
            yield from tasks_in(nested)
    elif isinstance(value, list):
        for nested in value:
            yield from tasks_in(nested)


class GrowthContractTests(unittest.TestCase):
    def setUp(self):
        self.source = yaml.safe_load(SOURCE.read_text())
        self.tasks = list(tasks_in(self.source))

    def task(self, name):
        return copy.deepcopy(next(task for task in self.tasks if task["name"] == name))

    def run_playbook(self, play, extra_files=None, options=()):
        executable = shutil.which("ansible-playbook")
        self.assertIsNotNone(executable, "Run in the existing Ansible execution environment")
        with tempfile.TemporaryDirectory(prefix="elastic-growth-contract-") as folder:
            root = Path(folder)
            (root / "fixture.yml").write_text(yaml.safe_dump(play, sort_keys=False))
            for name, content in (extra_files or {}).items():
                (root / name).write_text(yaml.safe_dump(content, sort_keys=False))
            return subprocess.run(
                [executable, "-i", "localhost,hypervisor,", str(root / "fixture.yml"), *options],
                capture_output=True, text=True, timeout=60, check=False,
            )

    def test_every_assertion_condition_is_a_string(self):
        count = 0
        for task in self.tasks:
            assertion = task.get("ansible.builtin.assert")
            if assertion:
                conditions = assertion.get("that", [])
                conditions = conditions if isinstance(conditions, list) else [conditions]
                for condition in conditions:
                    self.assertIsInstance(condition, str, task["name"])
                    count += 1
        self.assertGreater(count, 0)

    def test_actual_default_tag_guard_accepts_only_complete_runs(self):
        guard = self.task("Refuse empty or ambiguous hypervisor selection")
        guard["tags"] = ["always"]
        play = [{"hosts": "localhost", "connection": "local", "gather_facts": False,
                 "tasks": [guard]}]
        for options, expected in [((), 0), (("--tags", "custom"), 2),
                                  (("--skip-tags", "custom"), 2)]:
            with self.subTest(options=options):
                result = self.run_playbook(play, options=options)
                self.assertEqual(result.returncode, expected, result.stdout + result.stderr)

    def test_actual_state_parser_then_actual_preservation_assertions(self):
        before = "Domain: 'demo-one'\n  state.state=1\n  state.reason=1\n\nDomain: 'demo-two'\n  state.state=5\n  state.reason=1\n"
        cases = [
            {"name": "unchanged", "raw": before, "count": 2, "failed": False},
            {"name": "missing-state", "raw": before.replace("  state.state=1\n", "", 1),
             "count": 1, "failed": True},
            {"name": "changed-state", "raw": before.replace("state.state=1", "state.state=5", 1),
             "count": 2, "failed": True},
        ]
        variables = {
            "fixture_cases": cases,
            "__elastic_growth_states_before": {"stdout": before},
            "__elastic_growth_block_after": {"stdout": "Capacity: 21474836480"},
            "elastic_vm_disk_target_gib": 20,
            "__elastic_growth_disk_before": {"stat": {"inode": 100, "dev": 20}},
            "__elastic_growth_disk_after": {"stat": {"inode": 100, "dev": 20}},
            "__elastic_growth_root_before": {"stdout": "demo-root-identity"},
            "__elastic_growth_root_after": {"stdout": "demo-root-identity"},
            "__elastic_growth_filesystem": {"stdout": json.dumps({"filesystem_bytes": 20000000000})},
            "__elastic_growth_domains_before": {"stdout_lines": ["demo-uuid-one", "demo-uuid-two"]},
            "__elastic_growth_domains_after": {"stdout_lines": ["demo-uuid-two", "demo-uuid-one"]},
            "__elastic_growth_source_before": {"stat": {"checksum": "demo-sha256"}},
            "__elastic_growth_source_after": {"stat": {"checksum": "demo-sha256"}},
        }
        parser = self.task("Parse paired native domain names and states for preservation checks")
        assertion = self.task("Verify the authorized capacity and preservation outcome")
        assertion.update(ignore_errors=True, register="fixture_result")
        case_tasks = [
            {"name": "Bind synthetic native output", "ansible.builtin.set_fact": {
                "__elastic_growth_states_after": {"stdout": "{{ fixture_case.raw }}"}}},
            parser,
            {"name": "Check parser cardinality", "ansible.builtin.assert": {"that": [
                "__elastic_growth_state_pairs_before | length == 2",
                "__elastic_growth_state_pairs_after | length == fixture_case.count"]}},
            assertion,
            {"name": "Check preservation assertion result", "ansible.builtin.assert": {"that": [
                "(fixture_result.failed | default(false)) == fixture_case.failed"]}},
        ]
        play = [{"hosts": "localhost", "connection": "local", "gather_facts": False,
                 "vars": variables, "tasks": [{"name": "Exercise native-output cases",
                 "ansible.builtin.include_tasks": "case.yml", "loop": "{{ fixture_cases }}",
                 "loop_control": {"loop_var": "fixture_case", "label": "{{ fixture_case.name }}"}}]}]
        result = self.run_playbook(play, {"case.yml": case_tasks})
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
