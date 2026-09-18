# Growr skills

OpenClaw skills for read-only Solana discovery, token screening and wallet
investigations. Growr is a separately installed dependency; its code and
provider credentials are not included in this repository.

| Skill | Use it for |
| --- | --- |
| `growr-discover` | Find exact mints or browse Jupiter and Stonkfun feeds. |
| `growr-screen` | Translate research criteria into auditable shortlists. |
| `growr-investigate` | Inspect holder samples, wallets, overlap and activity. |

## Install Growr

This skills release targets Growr **0.3.x**, CLI schema **2.2**, playbook
contract **1.1**, screening **1.0**, and doctor **1.0**. The dependency pin
is `v0.3.0`.

```bash
uv tool install "git+https://github.com/drzerotrust/growr.git@v0.3.0"
growr --version
growr doctor --json --min-version 0.3.0 --max-version 0.4.0 \
  --require-cli-schema 2.2 --require-playbook-version 1.1 \
  --require-screening-version 1.0
```

For local development, install a Growr checkout:

```bash
uv tool install /absolute/path/to/growr
```

Alternatively use a Python 3.10+ virtual environment and
`python -m pip install /absolute/path/to/growr`. Make that environment's
`growr` executable available on the OpenClaw execution PATH. A normal install
must be repeated after source changes; use an editable install for development.

Each skill declares `metadata.openclaw.requires.bins: ["growr"]` and a uv
installer hint for the pinned release. Binary presence does not validate
version compatibility or install the dependency automatically. Each skill's
offline doctor preflight rejects incompatible versions/contracts. The
project-owned `compatibility.json` drives CI; OpenClaw does not parse it.

## Configuration

Set provider variables in the execution environment, or set `GROWR_ENV_FILE`
to an absolute path to a private dotenv file. Existing environment values
take precedence. Without an explicit file, Growr uses its checkout `.env`
when present, otherwise `$XDG_CONFIG_HOME/growr/.env` or
`~/.config/growr/.env`. It does not search arbitrary working directories.

Jupiter discovery needs `JUPITER_API_KEY`; `HELIUS_API_KEY` selects Helius
RPC, or `SOLANA_RPC_URL` supplies a custom endpoint. Public RPC and Stonkfun
search need no keys. Offline reranking needs no providers. Never commit keys,
embed them in commands, or copy dotenv contents into an agent response.

## Load the skills

Clone this repository, then merge its absolute directory into OpenClaw's
`skills.load.extraDirs`. The clone root directly contains the three skill
folders; there is no additional `skills/` level in this repository.

```json
{
  "skills": {
    "load": {"extraDirs": ["/absolute/path/to/growr-skills"]}
  }
}
```

The development layout may nest this repository at `/path/to/growr/skills`;
use that directory instead when appropriate. Git histories remain separate.
For a sandbox, install Growr and supply configuration inside that sandbox
as well; the host executable and host environment are insufficient.

```bash
openclaw skills list --eligible
openclaw skills info growr-screen
openclaw skills check
```

See [OpenClaw skills](https://docs.openclaw.ai/tools/skills) and
[configuration](https://docs.openclaw.ai/tools/skills-config).

## Use

- “Find Jupiter candidates named JUP without RPC scans.”
- “Screen Stonkfun xstocks with $100k minimum liquidity and a website;
  rank by 24h volume and verify at most five mints.”
- “Inspect five sampled owners of this mint and their shared holdings.”

Reports preserve exact identities, amounts, coverage and evidence. A partial
report can exit zero. Social presence is not authenticity, holder samples
are not a full census, and overlap does not prove shared control or bundles.
Skills do not trade or submit transactions.

## Responses

The answer follows the question, with formats selected for each capability:

| Request | Default response |
| --- | --- |
| Identity lookup, search or feed browsing | Identity summary or candidate table with full mints and provider scope. |
| General screening or token comparison | Criteria, observed values, decisions and reasons for the order. |
| Offline reranking | Updated results from saved evidence, with original observation times. |
| Token holders | Sampled owner/account balances and other holdings when requested. |
| Wallet inventory | Token quantities, account addresses, program/state and completeness. |
| Shared holdings | Cohort overlap with per-owner amounts, known absence and unknown presence. |
| Wallet or token-account activity | Bounded signature timeline with execution and detail coverage. |
| One transaction | Outcome, fees, supported actions and missing evidence. |
| Mint or token-account inspection | Relevant state, quantities, authorities and attributed context. |

An explicit format takes precedence; a simple fact gets a direct answer.
Mixed questions combine the relevant sections. A memecoin target does not
turn a wallet inventory or transaction explanation into a market shortlist.

Memecoin shortlists default to compact “organic-ish” cards with full mints,
market cap, 24h volume, turnover, holder count, the reported top-20 share,
social links and up to five wallet/token-account pairs. Ranking prioritizes
distribution, then liquidity/turnover, then organic and social evidence.
Shared holders are highlighted; unavailable data stays unknown and results
are never padded. Ask for another format or ranking to override these defaults.
Symbols and emojis adapt to the workflow, findings and evidence gaps; the
examples do not prescribe fixed icons.

Memecoin results contain only token cards and an optional short heading.
With no matches, return “No matching tokens found.” Unavailable or incomplete
checks receive a brief status instead of a false no-match conclusion.
Filenames, evidence paths, scan summaries, filter recaps and routine footers
are omitted unless explicitly requested. Material token-specific warnings
and observed holder overlap stay in the affected cards.

## License

MIT. See [LICENSE](LICENSE).
