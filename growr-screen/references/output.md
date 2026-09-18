# Screening output

Select a shortlist, comparison, diagnostic or replay layout by the question.
A requested format wins, including raw Growr JSON. A one-fact answer does not
need a full report. Symbols and emojis are optional and should describe the
observed outcome, not suggest a blanket endorsement.
Memecoin shortlists use their results-only delivery rules instead of the
general filter, exclusion and scope summaries below.

## General shortlist

Use for criteria-based screening across any supported token category.

Lead with how many candidates matched in the examined scope. State the applied
hard conditions and ranking priorities briefly, including chosen thresholds.
Use a compact table or a short card per match:

```markdown
**[Source] screen — [N] matches from [examined count] candidates**
Conditions: [hard filters]. Order: [declared priorities].

| Position | Token / full mint | Relevant observations | Why here |
| --- | --- | --- | --- |
| [rank] | [SYMBOL — name], `[MINT]` | [values, units] | [ranking evidence] |

Excluded: [count and material reasons]. Unresolved: [count and missing checks].
Scope: [feed/page or input], [observation time], [coverage], [evidence path].
```

Choose measurements from the user's criteria and ranking. A stablecoin,
tokenized asset or ordinary token comparison does not inherit memecoin
concentration priorities, “organic-ish” wording or speculation boilerplate.
Do not invent defaults that change the user's decision.

Preserve `matches`, `other_matches`, `rejected` and `unknown` as
distinct outcomes. Show fewer results when fewer pass, explain zero matches
within the examined scope, and state displayed versus total passing counts.
Do not promote incomplete required evidence or provider failures into a pass.

## Explicit token comparison

Use for “compare these mints” or “which of these fits my criteria?”

Put the exact supplied mints in the table, including rejected or unresolved
ones, with their decision labels. Use columns for the requested observations,
source/scope and the decisive difference. For many fields, put one field per
row and one token per column. Keep each full mint visible in the headings or
a nearby identity key.

Explain why a candidate outranks another only under the stated priorities.
Distinguish ties and incomparable/missing measurements. Do not hide a supplied
token because it failed or turn a comparison into an unrelated market search.

## One-token criteria check

Use for “does this token pass?” or “why was this rejected?”

Lead with pass, fail or unresolved and the full mint. Show only the relevant
checks using `requirements` and their evidence:

| Check | Required | Observed | Outcome |
| --- | --- | --- | --- |
| [field with units] | [operator and threshold] | [value/source or unknown] | [pass/fail/unknown] |

A known failure can reject a candidate while other checks remain unknown.
Keep those unknowns visible. Do not force a ranked list or holder inventory
into a diagnostic response.

## Offline reranking

Use for saved `token_screen` or discovery evidence. State the input file,
original observation time/range and current evaluation time. Say “saved
evidence,” not a fresh market scan. Report the new decisions and order using
the appropriate shortlist or comparison layout.
For memecoin results, omit the filename and use a brief saved/stale qualifier
in the heading or affected field instead of this diagnostic preamble.

If an original screen is available, describe actual rank/decision changes
and their cause, such as revised criteria or expired freshness. A discovery
file has no prior Growr ranking to compare against. Never invent deltas or
claim new RPC verification: replay makes no network requests.

## Memecoin shortlist

For finding, listing or ranking memecoins for selection, additionally read
[memecoin cards]({baseDir}/references/memecoin-output.md). Its field choices,
distribution-first defaults and turnover presentation apply to that profile.
Return only token cards, or its one-line empty/unavailable status. Do not add
filenames, process narration, filter/ranking recaps, exclusions or a footer.
They do not replace a focused comparison or diagnostic layout merely because
one token is a memecoin.

## Evidence and delivery

Read [interpretation]({baseDir}/references/interpretation.md) for decision,
coverage and source rules. Keep raw mint addresses and original report
decisions intact. Present the relevant measurements and gaps compactly.
General reports can include a scope/evidence footer and request use;
results-only memecoin responses omit them.

If JSON is requested, provide the actual supported report or its saved path
as requested; do not silently substitute an invented response schema. Display
preferences do not authorize extra lookups, broader limits or live refreshes.
