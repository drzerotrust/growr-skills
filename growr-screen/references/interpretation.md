# Read a screening report

Reports use playbook_version 1.1, playbook token_screen, screening_version 1.0.
Growr child reports remain CLI schema 2.2. Process success alone does not mean
complete evidence; usable partial reports exit zero.

- `criteria` records the requested conditions and priorities.
- `scope` records pages or explicit mints, candidate counts and omissions.
- `matches` contains up to `--top` passing candidates, with `other_matches`
  preserving additional passing candidates. `unknown` and `rejected` retain
  unresolved conditions and known failures separately.
- Every candidate contains evaluated `requirements`, ordered `ranking`
  measurements, source/scope/time provenance, and pointers into `evidence`.
  Conditions retain the threshold as `expected` and observation as `value`.
- `evidence` retains original public records, including separate pools for a
  repeated mint; raw provider envelopes are excluded.
- `scans` holds current child receipts. On offline replay, original child
  indices refer to `scope.source_scans` instead; no child is run again.
- `budget` separates conservative reservations from observed counters and
  unmeasured children. Each attempted RPC mint scan reserves four calls;
  Stonkfun list reserves two HTTP calls; other discovery reserves one.
  Reservations are not refunded after timeouts or lighter-than-expected reads.

The default initialized-mint requirement keeps candidates unverified by RPC in
`unknown`. Explicit provider-only screening can pass provider requirements
without RPC. Missing RPC facts never become proof of revocation or safety.

Numeric comparisons use decimal arithmetic. Fresh, usable Jupiter market data
takes precedence where the field is available. Independent Stonkfun pools are
retained; conflicting comparable pool values remain unknown. Never add repeated
token-level liquidity or present it as pool-level executable liquidity.

A failed hard requirement rejects a candidate even if another condition is
unknown. Missing ranking values do not become zero; complete ranking inputs
sort first. There is no hidden weighted “good token” score or return forecast.
Report ties and the declared priority order.

Offline reranking accepts a saved Growr discovery 2.2 report or a token_screen
1.0 report, up to 10 MiB. It recomputes values and decisions at the current
evaluation time; changed freshness can change the result. It does not trust
cached rankings. Original scope/times remain visible. Saved reports are local
evidence artifacts, not cryptographically authenticated chain proofs.

A concise answer should state: examined source and count; matching mints and
reasons; failures and unknowns; freshness and sample limits; request use; and
the saved report path. Select the layout from
[screening output]({baseDir}/references/output.md). For memecoin shortlists, follow
[the output standard]({baseDir}/references/memecoin-output.md): cards carry
the evidence, with compact notes for exclusions and scope. Its derived turnover
can refine presentation order across all passing candidates; preserve the
saved playbook order and identify any presentation reranking. A follow-up
holder or activity investigation remains a separate bounded workflow.
