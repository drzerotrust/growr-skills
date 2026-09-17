"""Check skill dependencies against an installed Growr without network."""

import json
import os
import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMPATIBILITY = json.loads((ROOT / "compatibility.json").read_text())
SKILLS = ("growr-discover", "growr-screen", "growr-investigate")


class SkillCompatibilityTests(unittest.TestCase):
    """Validate declarations and actual installed command behavior."""

    def setUp(self):
        """Use a private empty configuration and an unrelated cwd."""

        self.directory = tempfile.TemporaryDirectory(prefix="growr-skills-")
        self.addCleanup(self.directory.cleanup)
        self.folder = Path(self.directory.name)
        config = self.folder / "empty.env"
        config.write_text("")
        self.environment = dict(os.environ, GROWR_ENV_FILE=str(config))
        self.executable = shutil.which("growr")
        self.assertIsNotNone(
            self.executable, "Install Growr and add it to PATH"
        )

    def command(self, *arguments):
        """Run the installed executable and capture only public output."""

        return subprocess.run(
            [self.executable, *arguments],
            cwd=self.folder,
            env=self.environment,
            capture_output=True,
            text=True,
            check=False,
            timeout=30,
        )

    def test_metadata_and_references(self):
        """Ensure each separately published folder is self-contained."""

        dependency = COMPATIBILITY["growr"]
        source = "git+%s@%s" % (dependency["repository"], dependency["ref"])
        for name in SKILLS:
            folder = ROOT / name
            text = (folder / "SKILL.md").read_text()
            metadata = next(
                line.removeprefix("metadata: ")
                for line in text.splitlines()
                if line.startswith("metadata: ")
            )
            declaration = json.loads(metadata)["openclaw"]
            self.assertEqual(declaration["requires"], {"bins": ["growr"]})
            self.assertEqual(declaration["install"][0]["package"], source)
            references = re.findall(r"\]\(\{baseDir\}/([^)]*)\)", text)
            self.assertTrue(references)
            for reference in references:
                path = (folder / reference).resolve()
                self.assertTrue(path.is_relative_to(folder.resolve()))
                self.assertTrue(path.is_file(), reference)

    def test_installed_contracts(self):
        """Verify the release range and every required JSON contract."""

        dependency = COMPATIBILITY["growr"]
        contracts = COMPATIBILITY["contracts"]
        result = self.command(
            "doctor",
            "--json",
            "--min-version",
            dependency["minimum"],
            "--max-version",
            dependency["maximum_exclusive"],
            "--require-cli-schema",
            contracts["cli"],
            "--require-playbook-version",
            contracts["playbook"],
            "--require-screening-version",
            contracts["screening"],
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report["doctor_version"], "1.0")
        self.assertEqual(report["status"], "success")
        self.assertEqual(report["contracts"], contracts)
        self.assertFalse(report["network_checked"])
        self.assertTrue(all(report["playbooks"].values()))
        self.assertEqual(result.stderr, "")

    def test_incompatible_version_fails(self):
        """A present executable must not silently pass a wrong version."""

        result = self.command("doctor", "--json", "--min-version", "999.0.0")
        self.assertEqual(result.returncode, 1)
        self.assertEqual(json.loads(result.stdout)["status"], "error")

    def test_all_playbook_commands(self):
        """Every advertised playbook is available without a checkout."""

        for name in (
            "token-screen",
            "token-holders",
            "wallet-holdings",
            "shared-holdings",
            "activity",
        ):
            result = self.command("playbook", name, "--help")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("--json", result.stdout)

    def test_offline_screen(self):
        """Replay evidence without configuration or network requests."""

        from datetime import datetime, timezone

        mint = "So11111111111111111111111111111111111111112"
        record = {
            "kind": "token_discovery",
            "identity": {"chain": "solana", "mint": mint},
            "facts": {"source": "jupiter"},
            "coverage": [],
            "metrics": {
                "jupiter": {
                    "source": "jupiter",
                    "scope": "token",
                    "values": {"liquidity": 100000},
                }
            },
        }
        evidence = {
            "schema_version": "2.2",
            "tool": {"name": "growr"},
            "status": "success",
            "error": None,
            "records": [record],
            "coverage": [],
            "pagination": None,
            "request": {
                "command": "search",
                "target": None,
                "options": {"source": "jupiter"},
            },
            "run": {"completed_at": datetime.now(timezone.utc).isoformat()},
        }
        criteria = {
            "criteria_version": "1.0",
            "verify_on_chain": False,
            "requirements": [
                {"field": "liquidity_usd", "op": "gte", "value": "50000"}
            ],
        }
        for name, document in (("evidence", evidence), ("criteria", criteria)):
            (self.folder / ("%s.json" % name)).write_text(json.dumps(document))
        result = self.command(
            "playbook",
            "token-screen",
            "--input",
            "evidence.json",
            "--criteria",
            "criteria.json",
            "--json",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report["matches"][0]["mint"], mint)
        self.assertEqual(report["budget"]["subprocesses_attempted"], 0)
        self.assertEqual(result.stderr, "")


if __name__ == "__main__":
    unittest.main()
