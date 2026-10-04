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

After installing with uv, create the user configuration file as the same
user who will run Growr:

```bash
mkdir -p "${XDG_CONFIG_HOME:-$HOME/.config}/growr"
touch "${XDG_CONFIG_HOME:-$HOME/.config}/growr/.env"
chmod 600 "${XDG_CONFIG_HOME:-$HOME/.config}/growr/.env"
```

Edit that file to set `JUPITER_API_KEY` for Jupiter discovery and,
optionally, `HELIUS_API_KEY` for Helius RPC. The installer does not create
or populate the file. Run `growr doctor --json` after saving it to check
configuration locally; doctor does not validate credentials with providers.

Set provider variables in the execution environment, or set `GROWR_ENV_FILE`
to an absolute path to a private dotenv file. Existing environment values
take precedence. Without an explicit file, Growr uses its checkout `.env`
when present, otherwise `$XDG_CONFIG_HOME/growr/.env` or
`~/.config/growr/.env`. It does not search arbitrary working directories.

Jupiter discovery needs `JUPITER_API_KEY`; `HELIUS_API_KEY` selects Helius
RPC, or `SOLANA_RPC_URL` supplies a custom endpoint. Public RPC and Stonkfun
search need no keys. Offline reranking needs no providers. Never commit keys,
embed them in commands, or copy dotenv contents into an agent response.

Current Growr creates new snapshot/call databases at
`~/.config/growr/growr.db` (or `$XDG_CONFIG_HOME/growr/growr.db`) when storage
is first used. Existing `~/.growr/growr.db` is reused if the new default
database is absent. Older builds use that legacy location directly.
Set `GROWR_DATABASE_PATH` to an absolute filename in `.env` or the execution
environment to choose explicitly. Keep the same database across runs for
`fresh-calls` history; a separate database has separate recommendations.

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
- **“Run the degenerate Growr-skill playbook.”**
- “fresh-calls: find recent Jupiter tokens with $100,000–$1,000,000 market
  cap, good holder distribution, social presence and organic score. Use
  America/Mexico_City dates. If none qualify, show one weaker unreported
  candidate with its weakness. If none are eligible, say No good tokens scanned.”

The **degenerate** profile needs only that short instruction. It combines
Jupiter recent, trending, traded and organic-score feeds (1h for ranked
feeds), requires **$10,000–$500,000 market cap**, first-pool age up to
**48 hours**, and reported social presence. It samples up to 100 unique
mints and verifies up to 20 with a shared 80-RPC/four-discovery-HTTP budget.
The screening deadline is 600 seconds. The agent compares distribution,
liquidity and organic/social evidence, then returns the best one to three
unreported picks, or one eligible weaker pick with its known weakness.
Missing evidence is not automatically a weaker pick.

The profile automatically enables call history in **America/Mexico_City**;
you do not need to add `fresh-calls`. Explicit overrides, including disabling
history, win. With no eligible result it says `No good tokens scanned`;
assessment failures use a short failure/incomplete message. Final snapshot
bookkeeping may add up to three HTTP calls. See the
[saved recipe](growr-screen/references/degenerate.md). It requires a Growr
build whose `playbook token-screen --help` includes `--feeds`; the skill
checks this and reports an unavailable capability on older installations.

`fresh-calls` enables optional call history for `growr-screen`. It skips
mints recorded as reported today or yesterday and records only the final
selections. Outside the degenerate profile, screening without the keyword
can return previous picks. Explicitly disabling history always wins.
All runs must share a persistent Growr database. The mode checks for
`good-call --check`, `--if-new`, `--timezone` and `search --store-snapshot`
support; older pinned installations may need updating. See the skill's
[fresh-call workflow](growr-screen/references/fresh-calls.md) for commands
and date/delivery semantics.

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

Memecoin shortlists inspect up to ten candidates and return the strongest one,
two or three. Cards include full mints, market cap, 24h volume, turnover,
holder count, reported top-20 share and social platform names. Each card links
to `https://phantom.com/tokens/solana/<mint>` as `Open in Phantom`; these are
the only URLs in the memecoin output. Social platforms appear as names only,
such as `X · Telegram`, with website presence indicated separately when
reported. Ranking prioritizes distribution, then liquidity/turnover, then
organic and social evidence.
Stonkfun cards also show the reported trading pair, quote asset and quote mint
when available; missing pairing information stays unknown.
Unavailable data stays unknown and results are never padded. Keep the complete
response under 3,000 characters for delivery through a channel such as chat,
Discord or Telegram. Ask for another format or ranking to override these
defaults.
Symbols and emojis adapt to the workflow, findings and evidence gaps; the
examples do not prescribe fixed icons.

Memecoin results contain only one to three token cards and an optional short heading.
With no matches, return “No matching tokens found.” Unavailable or incomplete
checks receive a brief status instead of a false no-match conclusion.
Filenames, evidence paths, scan summaries, filter recaps and routine footers
are omitted unless explicitly requested. Material token-specific warnings
stay in the affected cards.

## License

MIT. See [LICENSE](LICENSE).
