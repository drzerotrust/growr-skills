"""Check skills against an installed Growr without network requests."""

import json
import os
import re
import shutil
import subprocess
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMPATIBILITY = json.loads((ROOT / "compatibility.json").read_text())
SKILLS = ("growr-discover", "growr-screen", "growr-investigate")


def degenerate_evidence(market_cap="10000", age=12, social=True):
    """Supply public evidence to exercise the saved profile offline."""

    now = datetime.now(timezone.utc)
    mint = "So11111111111111111111111111111111111111112"
    market = {
        "kind": "token_discovery",
        "identity": {"chain": "solana", "mint": mint},
        "facts": {"source": "jupiter"},
        "coverage": [],
        "metrics": {
            "jupiter": {
                "source": "jupiter",
                "scope": "token",
                "values": {
                    "market_cap": market_cap,
                    "liquidity": 50000,
                    "organic_score": 80,
                    "first_pool": {
                        "createdAt": (now - timedelta(hours=age)).isoformat()
                    },
                },
            }
        },
        "social": {
            "coverage": {"jupiter": "success"},
            "platforms": ["twitter"] if social else [],
            "score": 80,
        },
    }
    token = {
        "kind": "token",
        "identity": {"chain": "solana", "mint": mint, "address": mint},
        "facts": {
            "source": "rpc",
            "mint": {"initialized": True, "supply": "1000"},
            "holders": {"top_twenty_percent": 12},
        },
        "metrics": {},
        "coverage": [],
    }
    evidence = []
    for record in [market, token]:
        evidence.append({"record": record, "retrieved_at": now.isoformat()})
    return {
        "playbook_version": "1.1",
        "playbook": "token_screen",
        "screening_version": "1.0",
        "status": "success",
        "scope": {"selected_mints": [mint]},
        "evidence": evidence,
    }


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
        """Capture public output from the installed executable."""

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
        """Reject an incompatible executable version."""

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

    def test_degenerate_saved_profile_filters_public_evidence(self):
        """Check market-cap, age and social rules through Growr."""

        asset = ROOT / "growr-screen" / "assets" / "degenerate.json"
        cases = [
            ("10000", 12, True, "matched"),
            ("500000", 12, True, "matched"),
            ("9999.99", 12, True, "rejected"),
            ("500000.01", 12, True, "rejected"),
            ("10000", 47.99, True, "matched"),
            ("10000", 48.01, True, "rejected"),
            ("10000", 12, False, "rejected"),
            (None, 12, True, "unknown"),
        ]
        for cap, age, social, outcome in cases:
            with self.subTest(cap=cap, age=age, social=social):
                evidence = degenerate_evidence(cap, age, social)
                path = self.folder / "profile-evidence.json"
                path.write_text(json.dumps(evidence))
                result = self.command(
                    "playbook",
                    "token-screen",
                    "--criteria",
                    str(asset),
                    "--input",
                    str(path),
                    "--json",
                )
                self.assertEqual(result.returncode, 0, result.stderr)
                report = json.loads(result.stdout)
                self.assertEqual(report["counts"][outcome], 1)
                self.assertEqual(report["budget"]["subprocesses_attempted"], 0)
                self.assertEqual(result.stderr, "")

    def test_degenerate_missing_distribution_is_not_complete_ranking(self):
        """Passing numeric filters alone does not establish quality."""

        evidence = degenerate_evidence()
        evidence["evidence"][1]["record"]["facts"].pop("holders")
        path = self.folder / "incomplete-evidence.json"
        path.write_text(json.dumps(evidence))
        asset = ROOT / "growr-screen" / "assets" / "degenerate.json"
        result = self.command(
            "playbook",
            "token-screen",
            "--criteria",
            str(asset),
            "--input",
            str(path),
            "--json",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report["status"], "partial")
        self.assertFalse(report["matches"][0]["ranking_complete"])
        self.assertIsNone(report["matches"][0]["ranking"][0]["value"])


if __name__ == "__main__":
    unittest.main()
