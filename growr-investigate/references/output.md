# Investigation output

Choose the section matching the question, regardless of whether the target is
a memecoin, another token, a wallet or a program authority. User-specified
formats win. Answer single facts directly; combine only relevant sections for
mixed questions. Symbols and emojis are optional and reflect actual findings.

| Question | Output section |
| --- | --- |
| Who is in this token, and what else do they hold? | Sampled holders |
| What does this wallet own; where are its token accounts? | Wallet holdings |
| What assets do these sampled wallets share? | Shared holdings |
| What recently referenced this wallet or token account? | Activity or history |
| What happened in this signature? | One transaction |
| What is this mint's state or reported context? | Mint inspection |
| What is this token account, and what can it do? | Token-account inspection |

Use full supporting mints, wallet/account addresses and signatures. Quantities
come from exact strings and known decimals; unresolved units stay labelled raw
units. Preserve source, time and coverage. Read
[evidence rules]({baseDir}/references/evidence.md) for interpretation limits.
Templates below illustrate layouts, not mandatory text or extra data requests.

## Sampled holders

Use `token_holders` for an owner investigation or existing token-scan
evidence for a question limited to its largest accounts.

Lead with the target mint and sample scope: returned token accounts, selected
owners, unresolved owners and any omitted owners. Then use owner cards:

```markdown
**Holder sample — `[MINT]`**
[Returned accounts]; [selected owners]; [unresolved accounts].

**Owner `[WALLET]` — [inventory status]**
Target in initial sample: [exact amount] tokens.
Sample accounts: `[TOKEN_ACCOUNT]` — [its exact amount] tokens.
[Repeat contributing accounts when the owner has more than one.]

Other holdings, when asked:
| Token | Mint | Amount | Units / coverage |
| --- | --- | --- | --- |
| [reported symbol/name] | `[MINT]` | [exact amount] | [known units or unresolved] |
Accounts: [full account addresses and the amounts/states behind each holding].
```

Keep the sample rank and sample total distinct from the later wallet's target
balance. Never attach an aggregate owner's amount to a single account.
If using token-scan rows directly, label them largest accounts, not a
deduplicated owner ranking. Failed inventories leave the sampled owner
visible with an unavailable inventory; they do not mean the owner holds
nothing. Do not add price, turnover or an investment ranking.

Highlight exact owner overlap across already examined mints when it answers
the question. Unresolved owners and protocols remain distinct from people;
the sample is not a holder census or proof of shared control.

## Wallet holdings

Lead with the full wallet address, SOL balance and inventory completeness.
Use `wallets[].holdings` for a playbook; a direct wallet scan instead
exposes `facts.token_accounts.entries` with account-level raw balances.

```markdown
**Wallet — `[WALLET]`**
SOL: [amount or unknown]. Inventory: [complete/partial/unavailable].

| Token / mint | Program | Token amount | Token accounts / state |
| --- | --- | --- | --- |
| [symbol/name], `[FULL_MINT]` | [SPL/Token-2022] | [exact amount or labelled raw units] | [full addresses and states] |
```

Keep mint/program groups separate and preserve their contributing accounts.
When the question is only how to find token accounts, use one row per account
with mint, program and state; metadata or market data is unnecessary.
Disclose omitted rows and zero balances when relevant. Do not rank holdings
by token quantity across different mints or invent a USD portfolio total.

A complete empty inventory, partial inventory and unavailable inventory
require different conclusions. Highlight frozen states and unit conflicts.
A target token label is relevant only when the wallet is being inspected in
the context of that target; other assets are simply holdings.

## Shared holdings

Use a saved holder cohort, not a market leaderboard. Lead with the original
target mint, selected-owner count, complete inventories and source observation
window. Show `shared_holdings` by mint/program with its cohort denominator:

```markdown
**Shared holdings — [selected owners] sampled owners**
Source: [saved report and its observation window].

| Asset / full mint | Observed owners | Known absent | Unknown presence |
| --- | --- | --- | --- |
| [asset], `[MINT]` | [owner_count / selected_owner_count] | [count] | [count] |

For `[MINT]`:
- `[OWNER]`: [exact quantity] via `[TOKEN_ACCOUNT]` [state].
```

Show the exact supporting owner/account amounts for each overlap of interest.
Separate the cohort's target token and known common assets from other overlaps.
An unlabelled asset is not automatically rare. Keep `decimals_conflict`
visible, and do not sum incompatible units. `unknown_presence` is not
absence; `known_absent` applies only to complete inventories in this sample.

This analysis is offline: preserve the saved times and zero network use.
Empty overlap means none was observed within the available cohort, not that
wallets have no relationship. Overlap alone is not a bundle or shared-control
finding.

## Activity or history

Lead with the exact addresses queried and the bounded window. Distinguish a
primary wallet from explicitly selected token accounts. Present unique
signatures in a timeline, newest first where slots/times establish order:

| Block time / slot | Signature | Execution | Observed action | Referenced addresses / detail coverage |
| --- | --- | --- | --- | --- |
| [time or unknown; slot] | `[FULL_SIGNATURE]` | [success/failed/unknown] | [supported event or unknown] | [full queried addresses; body status] |

For `activity`, use `windows`, `transactions`, each transaction's
`references`, and its body/`detail_status`. For direct `history`,
use `facts.entries` and `facts.pagination`. Keep execution outcome
separate from body retrieval status. Signature-only results cannot establish
a transfer or trade. Failed execution does not establish completed transfers.

Include missing bodies, continuation cursors, stopping reasons and budget
use in one compact scope footer. A signature referenced by multiple queried
addresses appears once with all those references. Block time, retrieval time
and slot are different observations. Do not turn address history into a claim
of complete wallet lifetime activity or call a balance change a purchase.

## One transaction

Lead with the full signature, execution outcome, slot and block time when
available. Identify fee payer, signers and fee if returned. Show supported
events with from/to accounts, asset or mint, exact amount and instruction
position where needed to explain what happened.

Use `facts.transaction`, including its `events` and recording gaps.
Separate decoded instructions from established completed actions. For failed
execution, explain the failure evidence and fee without presenting intended
transfers as completed. Missing bodies, logs, balance sides or unsupported
instructions remain explicit gaps.

Show relevant pre/post balance observations only if present, with unknown
sides preserved. SOL fees may be displayed from exact lamports; no USD
valuation or profit-and-loss calculation is implied. Do not add holder
rankings or token-selection cards to a signature explanation.

## Mint inspection

Lead with the full mint, reported name/symbol and program. Use a concise facts
table for the requested state: initialization, exact supply and decimals,
mint authority and freeze authority. A null authority and a missing field
are different findings.

If distribution is requested, show the reported top-20 largest-account share
and relevant holder rows from `facts.holders`, with sample limitations.
Provider market/social/audit context stays attributed and separate from RPC
facts. A reported risk score is not a probability of loss or a buy decision.

For Stonkfun burns or rewards, select only the relevant reported totals,
units and source times. A rewards comparison describes an observed cumulative
delta and normalized interval rate, not a wallet payout forecast. Missing
provider context is unknown; do not invent a per-holder payment.

## Token-account inspection

Lead with the full token-account address, mint, owner authority and token
program. Show raw balance, exact token units only when decimals are known,
account state, delegate and close authority as relevant to the question.
Keep the owner authority distinct from the owning program.

Owner SOL balance and signature context returned by `token-account` belong
to that owner. They are not the token account's own history. A question about
the account's activity uses the activity/history layout for that exact
address. SPL and Token-2022 base decoding does not establish that every
extension has been inspected.

## Delivery and scope

Finish with the observation window, relevant source/commitment/context slots,
coverage gaps and evidence path when available. Report measured requests
separately from upper estimates when cost is part of the question. Avoid
repeating generic caveats after every row.

Keep empty, unknown, partial and failed results distinct. Preserve useful
evidence on partial runs and label any displayed subset. Do not fetch
unrequested markets, inventories or transactions merely to fill a format.
If raw JSON is requested, use the actual Growr report or its saved path as
requested instead of inventing a schema. No investment ranking or memecoin
disclaimer is required for an ordinary factual investigation.
