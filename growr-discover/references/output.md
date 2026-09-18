# Discovery output

Choose the layout by the question. These are guides, not forms to fill with
unrelated fields. A requested format wins, including raw Growr JSON. Answer a
single-fact question directly. Symbols and emojis are optional and contextual.

## Identity lookup

Use for “What mint is this?”, an exact-mint lookup, or checking a name/symbol.

Lead with the identity: token name, reported symbol and full mint. Add the
provider and whether the request was an exact mint or a text query. Include
only requested metadata, such as a reported website or token program.

A text query can return several assets with the same symbol. List the distinct
mints and relevant identifying evidence; do not silently select one. An exact
mint lookup that returned no match is “not found in this provider response,”
not proof that the mint does not exist on-chain. Provider lookup failure is
unavailable evidence, not a successful empty search.

Do not attach holder rankings, risk judgments or memecoin cards to a simple
identity question.

## Search candidates

Use for general name/symbol searches or finding candidates without filters.

Suggested layout:

```markdown
**Search: [query] — [provider], [returned count] candidates**

| Token | Mint | [Relevant available field] |
| --- | --- | --- |
| [SYMBOL — name] | `[FULL_MINT]` | [value and units] |

Scope: [query/page], [retrieval time], [coverage or omissions].
```

Keep returned candidates distinct and preserve provider order. Choose columns
that answer the question; market cap, liquidity or a reported social link may
be useful, but are not mandatory. An exact mint is always visible for each
token. Results are candidates, not verified matches to untested conditions.

## Feed listing

Use for “show recent tokens,” “list Stonkfun xstocks” or a provider-ranked feed.

State provider, feed/category, requested ranking interval and page. A compact
table can show provider position, token, full mint and the relevant market
measurements. Identify provider order explicitly; feed position is not a
Growr quality score. Label volume periods and distinguish recent pool
creation from mint creation.

Retain pool identity when multiple Stonkfun rows refer to the same mint.
Grouping those rows for readability must not merge incompatible measurements
or duplicate token liquidity. Show displayed versus returned counts and any
known pagination; do not imply that one page is the whole market.

## Memecoin lists and requests for “best”

For a memecoin list or shortlist, read
[memecoin cards]({baseDir}/references/memecoin-output.md). Discovery-only
cards use the discovery heading and make untested distribution visible.
This is a conditional presentation profile, not a reason to run more RPC.

Criteria-based “best,” “safer,” or ranked selection belongs to the screening
workflow. Do not relabel a discovery feed as a passed screen. User-specified
formats or focused identity questions retain the layouts above.

## Evidence and gaps

Use the existing report only: full identities, relevant source/scope,
retrieval time and coverage. Include a saved-evidence path if one was created,
never invent one. Keep zero distinct from unknown and returned-empty distinct
from failed. Show the actual result count without padding. Do not request
metadata, holder data or a new provider merely to fill a display column.
