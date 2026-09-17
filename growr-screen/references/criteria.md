# Criteria 1.0

The runtime is `scripts/playbooks/token_screen.py`. Use one of `--provider`,
`--mints MINT [MINT ...]`, or `--input FILE`, plus `--criteria FILE`.

```json
{
  "criteria_version": "1.0",
  "verify_on_chain": true,
  "max_age_seconds": 900,
  "requirements": [
    {"field": "liquidity_usd", "op": "gte", "value": "100000"},
    {"field": "has_website", "op": "eq", "value": true},
    {"field": "has_social", "op": "eq", "value": true},
    {"field": "freeze_authority_revoked", "op": "eq", "value": true}
  ],
  "ranking": [
    {"field": "volume_24h_usd", "direction": "desc"},
    {"field": "liquidity_usd", "direction": "desc"}
  ]
}
```

This is an example research profile, not a default investment strategy. Use
the user's conditions. All requirements are ANDed. Numeric operators: eq,
gte, lte, gt, lt. Boolean and category requirements support only eq. Numeric
thresholds can be exact decimal strings. Ranking uses numeric fields with
asc/desc in priority order; exact mint breaks ties. Missing ranking inputs
sort after complete ranking inputs and remain visible.

| Field | Meaning / source |
| --- | --- |
| `liquidity_usd` | Jupiter token liquidity, never a pool depth guarantee. |
| `market_cap_usd` | Prefer fresh Jupiter token market cap; otherwise Stonkfun pool-scoped market cap. |
| `volume_24h_usd` | Jupiter 24h buy + sell volume for Jupiter discovery; Stonkfun 24h volume for Stonkfun pool records. |
| `holder_count` | Jupiter-reported count, not a census independently performed by Growr. |
| `organic_score` | Jupiter's reported measure. |
| `social_score` | Growr's reported-link presence score, not authenticity. |
| `first_pool_age_hours` | Age of exposed Jupiter first-pool creation, not mint age. May be absent from Stonkfun enrichment. |
| `top_20_accounts_pct` | RPC largest-account sample's percentage of supply, not distinct owner concentration. |
| `has_website`, `has_social` | Reported presence from successful provider coverage. |
| `verified` | Jupiter's reported verification flag. |
| `initialized_mint` | RPC mint initialization flag. Required by default. |
| `mint_authority_revoked`, `freeze_authority_revoked` | Explicit null RPC authorities; missing fields are unknown. |
| `category` | Stonkfun quote category, not a general token taxonomy. |

`verify_on_chain` defaults to true and adds initialized_mint == true. Set false
for disclosed provider-only screening; explicit RPC requirements still require
RPC evidence. `max_age_seconds` defaults to 900 and accepts 1-604800. Age uses
provider update time where exposed, otherwise retrieval time, which does not
prove that a provider's cached measurement was recently refreshed.

Live discovery:

- Jupiter: `--provider jupiter --query JUP`; or `--feed recent`; or a ranked
  feed toptraded/toptrending/toporganicscore with `--interval 5m|1h|6h|24h`.
- Stonkfun: `--provider stonks --feed recent|marketCap|volume`, optionally
  `--category xstock|prestock|custom|collectibles|currencies|leverage`.
- Stonkfun query: `--provider stonks --query te --sort marketCap|volume|newest`.
  Queries reject category/feed/interval. Stonkfun alone accepts `--page`,
  `--pages` (1-10), and `--page-size` (1-100).

Limits: candidate-limit 1-100, scan-limit 0-20, top 1-100, max-rpc-calls 0-500,
max-http-calls 0-100, timeout 1-120, max-seconds 1-1800. Defaults are in SKILL.md.
Explicit mint market lookups use one Jupiter batch; RPC-only criteria need
no Jupiter request. Unknown keys/fields, nonfinite numbers, duplicate JSON
keys and incompatible CLI flags are rejected before children start.

Unsupported claims such as confirmed bundle membership, full owner history,
estimated wallet reward income, realized PnL or future returns must be explained
as unavailable, not mapped to a convenient surrogate field.
