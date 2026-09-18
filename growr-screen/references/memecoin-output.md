# Growr memecoin output standard

Use this profile for a memecoin list or shortlist: finding candidates,
screening a feed or ranking candidates for selection. Select the profile by
the user's question, not merely by a token's category. Identity lookups,
criteria diagnostics, explicit comparisons, wallet/holder investigations and
transaction explanations use their task-specific output unless the user asks
for these cards. An explicit format or ranking takes precedence. Keep CLI
JSON and saved evidence unchanged.

## Results-only delivery

Return token results, not a report about the work performed. This rule
overrides general instructions to include scope, methods or evidence footers.
Unless the user explicitly asks for diagnostics, explanation or evidence:

- With matches, return only the token cards and an optional short results
  heading. Keep material token-specific warnings, missing values and observed
  holder overlap within the affected cards.
- With a completed search and no matches, return only:
  `No matching tokens found.`
- If no match can be verified because required checks were unavailable,
  return only: `No verified matches; required checks were unavailable.`
- If the search could not run or discovery failed, return one short status,
  such as `Search unavailable: provider request failed.` Never report a
  failed search as a successful zero-match result.
- Do not include filenames, paths, artifact links, shell commands, scan/page
  counts, age-band counts, filter recaps, ranking explanations, request
  budgets, process narration, evidence references or routine disclaimers.
- Do not append reasons why nothing passed, summaries of rejected candidates,
  “no other listings passed,” follow-up offers or a closing paragraph.

Keep criteria, exclusions, provenance, timestamps and saved evidence in the
underlying reports. Use them to verify and rank candidates without copying
that bookkeeping into the response. Do not add narration before the result.

## Card format

Use one card per distinct mint, with the actual number returned in the header.
Fill placeholders from evidence; never print the template as a result.

Choose symbols and emojis to suit the workflow and observed results, not a
fixed palette. Discovery, a supported match, a coverage gap, a rejection and
an investigation finding can have different visual cues. Markers are optional:
use plain labels when clearer, and make their meaning explicit in nearby text.
Do not imply approval, certainty or momentum just because a template has an
icon. Token symbols remain the actual reported tickers.

```markdown
[CONTEXT_MARKER] **[Source] “organic-ish” screen — top [N]**

[RESULT_MARKER] **[SYMBOL] — [Token name]**

- Mint: `[MINT_ADDRESS]`
- Pair: **[SYMBOL] / [QUOTE_SYMBOL]** · [QUOTE_NAME] · [QUOTE_CATEGORY]
- Quote mint: `[QUOTE_MINT]`
- **$[MARKET_CAP] mcap** | **$[VOLUME_24H] 24h volume** | **[TURNOVER]% turnover**
- **[HOLDER_COUNT] holders** | **top 20: [TOP_20_SHARE]%** of supply (largest token accounts)
- **[Social account](SOCIAL_MEDIA_URL)**
- Top 5 holders (largest token accounts):
  - `[WALLET]` | `[TOKEN_ACCOUNT]`

    [AMOUNT_OF_TOKENS] tokens
- [FINDING_MARKER] [material finding, when present]
```

The Pair and Quote mint rows apply to Stonkfun listings; omit them for other
sources without pairing evidence. Omit missing optional quote name/category
labels rather than printing placeholders.

Repeat holder rows up to five times and cards for the actual results. Keep
full mint, wallet and token-account addresses. A wallet authority can be a
pool or program; the rows do not establish independent people. Positive
markers must reflect the stated filters and evidence, never a buy
recommendation. Make material concerns and unresolved checks visible even
when a candidate matches the filters.

Do not add a scope or evidence footer. Show source attribution in the short
heading or affected field when needed, and material uncertainty in the
affected card. Saved/stale observations must not be presented as current;
use a brief qualifier in the heading or field, without naming the input file.

For discovery-only requests, retain feed order and label the header
“discovery candidates — [N]” instead of claiming a ranked screen. Give
unevaluated candidates a neutral cue or plain status; disclose unverified
distribution. Do not expand a provider-only request into RPC work just to
complete the template.

## Populate from evidence

- Identity: use `identity.mint` and same-mint names/symbols from discovery or
  token metadata. A symbol match alone cannot join records. Group repeated
  Stonkfun pools into one mint card while retaining their separate evidence.
- Stonkfun pairing: display the reported pair from the same pool record's
  `identity.symbol` and `facts.quote_symbol`, with `facts.quote_name`
  and `facts.quote_category` when present. Show the full
  `facts.quote_mint` separately. In screening reports, follow the
  candidate's `evidence_indices` into `evidence[].record` and use the
  exact-mint Stonkfun pool record. These fields already arrive with listings;
  no additional API or RPC call is needed.
  Use an available name or full mint when a symbol is absent. If no quote
  identity is reported, show `Pair: unknown`; an absent quote mint is
  `Quote mint: unknown`. Never guess SOL, USDC or a quote token from the
  category, reward currency or another pool. If a mint has multiple returned
  pools, retain each pool's pair with its `identity.pool` address rather
  than choosing one silently. Describe only reported pairs, not every venue
  trading the mint or independently verified live pool contents.
- Market cap: use an explicit USD market-cap measurement, never FDV as a
  substitute. Jupiter exposes `metrics.jupiter.values.market_cap`;
  Stonkfun records expose `facts.market_cap_usd`. Sourced combined
  `metrics.market` values must retain their source and scope.
- 24h volume: Jupiter exposes `metrics.jupiter.values.activity["24h"]`
  with `buyVolume` and `sellVolume`; both must be known before summing.
  Stonkfun records expose `facts.volume_24h_usd`. Do not annualize or
  relabel a 5m/1h/6h feed interval as 24h volume.
- Turnover = 24h USD volume ÷ USD market cap × 100. Use decimal arithmetic,
  a positive market cap, nonnegative volume and compatible source, scope and
  observation time. Show zero only for a measured zero volume with a valid
  denominator. Missing, zero-cap, nonfinite or incompatible inputs mean
  `turnover: unknown`. Do not silently divide one pool's volume by another
  provider's token market cap or sum repeated token metrics across pools.
- Holder count: use the explicitly reported count with its provider coverage,
  such as `metrics.jupiter.values.holder_count` or the sourced
  `metrics.risk.holderCount.value`. Never use the number of sampled
  accounts or selected wallets as the total holder count.
- Top 20: use `facts.holders.top_twenty_percent` from an exact-mint RPC
  record with positive supply and usable holder coverage. Screening calls this
  `top_20_accounts_pct`. In listings the token record can be nested under
  `on_chain`; screening retains it in `evidence[].record`. This is the
  largest-account sample share, not a distinct-wallet share. If fewer than
  20 accounts were returned, say how many. Do not substitute a generic
  “top holders” audit percentage, top-ten share, largest-wallet share, or
  the sum of only the five displayed rows. Another source is usable only
  when its measure explicitly specifies top 20 and its population is stated.
- Social: show actual normalized `social.links` entries for the same mint,
  including a website when present. Make reported social links clickable and
  bold. Do not invent a handle from a symbol or label a link as authenticated.
- Missing values: write `unknown`, with one short reason when material.
  Do not render `$unknown`, `unknown%`, or guessed zeros. Missing social
  data is `Social: not reported` after a successful lookup, or
  `Social: unknown` after unavailable/failed coverage. If holder rows are
  unavailable, retain `Top 5 holders: unknown (not fetched / partial)`.
- Readable numbers: use separators for counts and balances; K/M/B is fine
  for USD amounts. Round displayed ratios only after calculation and preserve
  nonzero values smaller than the display precision as `<0.01%`. Keep exact
  holder token quantities; never round a small nonzero holding into zero.

## Holder rows and overlap

Reuse `facts.holders.top_accounts` from existing token evidence. Take the
first five largest returned accounts with positive balances. Each row uses
`owner`, `token_account` and `amount_tokens`; alternatively convert
`raw_amount` with that mint's verified `facts.mint.decimals` using exact
decimal arithmetic. Never use a float `ui_amount` when an exact value is
available. Unknown decimals mean labelled raw units, not a guessed balance.

Keep separate accounts even when their owner repeats. A missing owner is
`owner unresolved | TOKEN_ACCOUNT`; do not invent an associated account or
promote another row to conceal the gap. If using a token-holders playbook,
label its ranking “sampled owners” and retain every `sample_accounts` entry
and its amount. An owner's sample total must not be assigned to one account.

Match resolved owner addresses exactly across different mints. Highlight a
repeated wallet in bold with a suitable marker or “shared holder” label in
each affected card. Keep a compact overlap note within those cards, naming
the full wallet and the other symbols plus exact mints.
Compare all already available sample rows, not just the displayed five; if a
repeat is outside the five, mention it in the note without implying that it
is a top-five account. Report observed overlap, never coordinated buying,
independent wallets, shared control or a confirmed bundle.

Existing wallet inventory can also establish another positive holding:
retain its mint, token-account address, exact amount and observation time.
Distinguish this from membership in another token's top-holder sample.
Unknown inventories cannot establish absence. Do not add wallet scans or
transaction crawls merely to decorate a listing; use bounded investigation
when that additional scope is requested. Reuse evidence and respect the
total agreed request budget across commands.

## Filtering and ranking

Apply the user's hard filters first. Do not invent numerical cutoffs for
“good” or “organic-ish.” Resolve material ambiguity before running a screen;
keep the selected conditions in its criteria/evidence, without a filter recap
in the results. A required unknown is unresolved, not a pass.

Default memecoin priority is lexicographic:

1. Lower reported top-20 supply share.
2. Higher liquidity, then higher valid 24h turnover within the passed filters.
3. Stronger reported organic score, then social evidence.
4. Exact mint address to break remaining ties.

Unknown values sort after known values at the corresponding priority and
stay visible. Use comparable populations for distribution and compatible
sources/scopes for market comparisons. Holder count is context, not a
substitute for distribution. High turnover alone does not establish organic
activity; links show presence, not engagement or authenticity.

Criteria 1.0 supports `top_20_accounts_pct` ascending, `liquidity_usd`
descending, `organic_score` descending and `social_score` descending.
Use those declared priorities for the playbook when the user has not supplied
others. It does not support a `turnover` field. Compute turnover from retained
evidence for presentation; never send an invented field to the CLI. Consider
all passing candidates in `matches` and `other_matches`, apply the above
presentation order with derived turnover, then take N. Do not silently edit
saved decisions or claim that this is the playbook's original ordering.
Retain the derivation and presentation order in working evidence; explain
them only when requested, not in the default token results.

If the user requires a turnover threshold, evaluate it separately from the
CLI criteria on the same saved evidence; retain the applied threshold and its
pass/fail/unknown result there. Do not substitute volume for turnover or imply
an unsupported filter was enforced by Growr. Exclude unresolved required values
and known failures from passing cards.

Surface material disqualifiers concisely: reported transfer tax, inactive or
weak liquidity, live mint/freeze authority, extreme concentration, or
evidence-backed linked-wallet indicators. Attribute provider-only flags and
unknown authority/fee checks; absent warnings do not prove those checks passed.
Known violations of the user's filters are exclusions, not matches.
Overlap alone is an observation, not a suspicious-control finding. Use a
momentum cue only for a measured, time-bounded momentum observation.

Never pad a list with unknowns or rejected candidates. Check `other_matches`
before selecting the final cards. If only one or two passed, return only
those without explaining the shortfall. For zero matches or unavailable
results, use the one-line status rules above. Do not show placeholder cards
or promote unresolved candidates to fill the requested count.

“Organic-ish” is always a screening label, never a certainty, safety claim
or return forecast.
