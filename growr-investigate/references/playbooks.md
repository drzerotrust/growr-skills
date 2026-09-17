# Select a bounded workflow

Use the installed `growr` command. Playbook options follow the recipe
name; scan/discovery global flags precede their command.

| Question | Entry point | Default network upper bound |
| --- | --- | --- |
| Who appears in the token sample, and what else do they hold? | `growr playbook token-holders MINT --json` | 24 RPC + 10 Jupiter HTTP. |
| What does one wallet currently hold? | `growr playbook wallet-holdings WALLET --json` | 4 RPC + 10 Jupiter HTTP. |
| What assets overlap in a saved cohort? | `growr playbook shared-holdings holders.json --json` | Zero network calls. |
| What recently referenced these explicit addresses? | `growr playbook activity ADDRESS --json` | One default address: up to 11 RPC, zero provider HTTP. |
| Inspect one transaction | `growr --json transaction SIGNATURE` | One RPC. |
| Locate current token accounts | `growr --json wallet WALLET` | Four RPC. |
| Inspect a token account's state | `growr --json token-account ACCOUNT` | Three RPC; summary history is the owner's. |
| Inspect that token account's history | `growr --json history ACCOUNT --limit 10 --details` | Up to 11 RPC. |

Holder and wallet options: --no-jupiter, --jupiter-batch-limit (1-10, default
10), --mint-limit (0-50, default 0), --timeout (1-120, default 30 seconds per
child). Holder only: --wallet-limit (1-20, default 5). A metadata batch handles
up to 100 distinct mints; an extra RPC unit scan costs up to four RPC calls.

Activity options: --token-account may repeat up to ten times; --limit (1-100,
default 10) references per page; --pages (1-10, default 1) per address;
--transactions (1-100, default 20) unique bodies; --max-rpc-calls (1-500,
default 50) shared cap; --timeout (1-120, default 30). It reads pages first,
then bodies, deduplicating signatures across addresses. It does not discover
accounts or traverse counterparties automatically. Use direct `history
ADDRESS --before SIGNATURE` to continue a saved cursor.

Shared holdings accepts only a success/partial token_holders playbook 1.1
report up to 10 MiB. It is not an input adapter for CLI wallet reports or
wallet_holdings reports. It preserves original observation times.

Contracts: playbook 1.1; CLI 2.2. Partial reports can exit zero. Initial
failures exit one; argument errors normally exit two with plain-text usage.
