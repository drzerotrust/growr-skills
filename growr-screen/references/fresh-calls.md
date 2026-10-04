# Fresh calls: skip recent recommendations

Use when the user's task enables `fresh-calls` or selects the degenerate
profile, unless repeat suppression is explicitly disabled. This rule applies
to the final selections, including an explicitly requested weaker fallback.
Leave screening evidence and deterministic ranking unchanged.

## Meaning and prerequisites

- A saved snapshot is an observation, not proof of a recommendation.
  Check `GoodTokenCall` through the CLI. Only `status: reported` counts.
  Draft/rejected decisions and ordinary scans do not consume a mint.
- Match full mint addresses across providers, pools and agents sharing the
  same database. Symbols/names do not establish identity. The scope is the
  entire configured database; there is no per-channel or per-strategy filter.
- The window begins at yesterday's midnight and ends at the check time,
  including today, in the task/user's timezone. Use UTC if none is known.
  Pass the same `--timezone` to every check/save. This is two calendar
  dates, not a rolling 48-hour window. Old calls become eligible again.
- Every run must use the same persistent database. Current Growr defaults
  to `~/.config/growr/growr.db` (or `$XDG_CONFIG_HOME/growr/growr.db`) and
  reuses existing `~/.growr/growr.db` if the new default file is absent.
  Older builds use that legacy location directly. Set `GROWR_DATABASE_PATH`
  in the execution environment or selected `.env` to choose explicitly.
  A new database per run cannot prevent repeats. Do not read credentials
  or print database paths.
- After the ordinary doctor check, inspect `growr good-call --help` for
  `--check`, `--if-new`, `--timezone`, and `growr search --help` for
  `--store-snapshot`. Older 0.3.x installations can pass doctor but lack
  these features. If missing, return a brief dependency failure; do not
  silently disable repeat suppression or change the installation.

## Selection and recording

1. Screen normally with the user's criteria and request `--top 10` when
   available. Consider at most ten distinct ranked candidates. Look through
   `matches` and `other_matches`; inspect non-passing candidates only when
   the user explicitly allows a weaker fallback. Keep their actual decision.
2. For each candidate under consideration, check its mint:

   ```bash
   growr --json good-call <MINT> --check --timezone America/Mexico_City
   ```

   Require exit zero, `command: good-call`, `status: success`, the exact
   `data.mint`, and a boolean `data.already_reported`. If true, skip that
   mint and consider the next ranked candidate. A failed/malformed check
   is unknown history: stop with `Call history unavailable.` Do not treat
   it as a new token or use snapshots as a substitute.
3. Prepare the final picks and cards before recording anything. Prefer
   good matches; if none remain, use an unreported weaker fallback only
   when explicitly requested. Respect hard filters and show its weakness.
   If no eligible unreported candidate remains, use the user's exact empty
   sentence, or `No new matching tokens found.` Never recycle a recent
   mint just to fill the response or expand beyond the allowed scope.
4. Each pick needs a stored snapshot for the same mint. Reuse a snapshot
   already saved from this run if its identity and observation are known.
   Otherwise save a fresh exact-mint search, budgeting one extra HTTP call
   per pick and no extra RPC calls:

   ```bash
   growr --json search jupiter <MINT> --store-snapshot
   growr --json snapshot latest --mint <MINT>
   ```

   Use `search stonks` for a Stonkfun-only selection. Require a successful
   search with an exact-mint record. Require the snapshot's `data.mint`
   to match and `data.run` to equal the search response's `run.id`. If
   another run replaced the latest observation, do not attach its snapshot
   silently. Use `data.id` as the snapshot ID. Preserve original screening
   evidence; this is a new market observation, not a new on-chain check.
   Recheck any hard filters affected by changed market values before using
   it. If the HTTP budget is exhausted, stop instead of fabricating evidence.
5. Immediately before returning each selected card, save the call:

   ```bash
   growr --json good-call <MINT> --snapshot-id <ID> --if-new \
     --timezone America/Mexico_City --decision shortlist \
     --reasons 'Concise selection rationale'
   ```

   Use `--decision fallback` for a weaker pick; optional agent/strategy
   fields record attribution. `--if-new` sets `status: reported` and
   performs the check and insert together under a database write lock.
   Require exit zero, `status: success`, `data.created: true`, and a call
   with the exact mint/snapshot ID before including the card. If
   `data.created: false` and `data.already_reported: true`, another run
   reported it first: skip it and consider the next candidate within the
   same ten-candidate/request limits. Never record all screened candidates.

`reported` means committed to the final response. Growr does not send a
message or verify external delivery. If delivery fails after the save, the
mint remains suppressed for this window. Do not promise exactly-once message
delivery or retry by bypassing the guard. If some picks were saved before a
later failure, retain those picks in the response; do not silently replace
them with an empty-result sentence.

Keep all bookkeeping out of token cards: no database paths, snapshot IDs,
commands, duplicate counts or explanations of skipped tokens unless asked.
Keep the existing results-only, 3,000-character memecoin output limit.
