# Growr memecoin output standard

Use this profile for a memecoin list or shortlist: finding candidates,
screening a feed or ranking candidates for selection. Select the profile by
the user's question, not merely by a token's category. Identity lookups,
criteria diagnostics, explicit comparisons, wallet/holder investigations and
transaction explanations use their task-specific output unless the user asks
for these cards. An explicit format or ranking takes precedence. Keep CLI
JSON and saved evidence unchanged.

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
- **$[MARKET_CAP] mcap** | **$[VOLUME_24H] 24h volume** | **[TURNOVER]% turnover**
- **[HOLDER_COUNT] holders** | **top 20: [TOP_20_SHARE]%** of supply (largest token accounts)
- **[Social account](SOCIAL_MEDIA_URL)**
- Top 5 holders (largest token accounts):
  - `[WALLET]` | `[TOKEN_ACCOUNT]`

    [AMOUNT_OF_TOKENS] tokens
- [FINDING_MARKER] [material finding, when present]
```

Repeat holder rows up to five times and cards for the actual results. Keep
full mint, wallet and token-account addresses. A wallet authority can be a
pool or program; the rows do not establish independent people. Positive
markers must reflect the stated filters and evidence, never a buy
recommendation. Make material concerns and unresolved checks visible even
when a candidate matches the filters.

Use a short final scope line: source/feed/page or input file, observation
time/range, examined count, relevant gaps and evidence path. Include request
use when available. End with “Meme trades are speculation.” Do not add generic
risk paragraphs or repeat the same qualification under every card.

For discovery-only requests, retain feed order and label the header
“discovery candidates — [N]” instead of claiming a ranked screen. Give
unevaluated candidates a neutral cue or plain status; disclose unverified
distribution. Do not expand a provider-only request into RPC work just to
complete the template.

## Populate from evidence

- Identity: use `identity.mint` and same-mint names/symbols from discovery or
  token metadata. A symbol match alone cannot join records. Group repeated
  Stonkfun pools into one mint card while retaining their separate evidence.
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
each affected card. Add one compact overlap note naming the full wallet and
the other symbols plus exact mints.
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
“good” or “organic-ish.” Clarify material ambiguity; otherwise state the
chosen screening scope briefly. A required unknown is unresolved, not a pass.

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
Disclose once: “Presentation ranking includes derived 24h turnover.”

If the user requires a turnover threshold, evaluate it separately from the
CLI criteria on the same saved evidence; show the applied threshold and its
pass/fail/unknown result. Do not substitute volume for turnover or imply an
unsupported filter was enforced by Growr. Exclude unresolved required values
and known failures from passing cards.

Surface material disqualifiers concisely: reported transfer tax, inactive or
weak liquidity, live mint/freeze authority, extreme concentration, or
evidence-backed linked-wallet indicators. Attribute provider-only flags and
unknown authority/fee checks; absent warnings do not prove those checks passed.
Known violations of the user's filters are exclusions, not matches.
Overlap alone is an observation, not a suspicious-control finding. Use a
momentum cue only for a measured, time-bounded momentum observation.

Never pad a list with unknowns or rejected candidates. Check `other_matches`
before declaring that too few passed. If only one or two passed, return only
those and say “No other current listings in the examined scope passed.”
Add the unresolved/unscanned count when relevant. On offline evidence say
“saved listings,” not “current.” Zero matches means no matching cards. A failed
discovery is an unavailable result, not proof that no tokens qualify.

“Organic-ish” is always a screening label, never a certainty, safety claim
or return forecast.
