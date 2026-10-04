# Degenerate: saved Jupiter screening recipe

“Run the degenerate Growr-skill playbook” selects this entire recipe. No
additional explanation, `fresh-calls` keyword or clarification is needed.
Honor explicit overrides, including disabling repeat suppression. Apply
overrides to a separate working criteria file; leave the installed asset
unchanged. Do not make these defaults universal for other screens.

## Defaults

| Setting | Value |
| --- | --- |
| Source | Jupiter; recent, toptrending, toptraded, toporganicscore |
| Ranked-feed interval | 1h; recent has no interval |
| Market cap | $10,000–$500,000 inclusive |
| First-pool age | 0–48 elapsed hours; not mint age |
| Social presence | Required reported social link; a website alone is insufficient |
| Evidence freshness | 900 seconds, using Growr's existing timestamp rules |
| Ranking | Lower top-20 account share, higher liquidity, organic score, social score |
| Candidate sample | At most 100 distinct mints across all four feeds |
| Additional token scans | At most 20; 80 RPC calls reserved |
| Discovery HTTP budget | Four calls; one per feed, no retries |
| Child timeout / screening deadline | 30 / 600 seconds |
| Final review / output | Top ten candidates; one to three strong picks, or one weaker fallback |
| Repeat suppression | Enabled; reported GoodCalls today or yesterday |
| Calendar timezone | America/Mexico_City |

The timezone controls GoodCall dates; token age remains a rolling 48-hour
window. A `pass` means the hard requirements passed, not that the token is a
strong investment. Quality assessment belongs to the agent. Meme trades are
speculation; do not invent concentration or organic-score cutoffs.

## Preflight and execution

Run the normal doctor preflight. Check `growr playbook token-screen --help`
for `--feeds`. Unless repeat suppression was explicitly disabled, also run
the capability checks in [fresh calls]({baseDir}/references/fresh-calls.md).
An older 0.3.x build may pass doctor without these features. If missing,
report a short dependency failure; do not silently run a single feed, turn
off history or upgrade the installation. Jupiter requires its configured
key. Do not read credentials. Keep call history in the same persistent
database on every run.

Use the asset path resolved from this skill's base directory:

```bash
growr playbook token-screen \
  --provider jupiter \
  --feeds recent toptrending toptraded toporganicscore \
  --interval 1h \
  --criteria "{baseDir}/assets/degenerate.json" \
  --candidate-limit 100 \
  --scan-limit 20 \
  --max-rpc-calls 80 \
  --max-http-calls 4 \
  --timeout 30 \
  --max-seconds 600 \
  --top 10 \
  --json
```

The playbook queries each feed once and alternates between feed orderings
to sample unique mints. It retains repeated observations for selected mints,
then evaluates hard requirements and prioritizes bounded RPC verification.
It does not search every Jupiter token or verify every returned candidate.
The 1h feed interval does not replace the 24h volume used in token cards.

Retain the JSON and any reasoning in working evidence. Do not overwrite
previous evidence. Inspect `scope.feeds`, candidate omissions, `counts`,
`gaps`, `budget`, per-candidate conditions and ranking coverage before
choosing cards. Feed failures and verification limits must stay visible in
the evidence even when usable results remain.

## Selection and history

Read [memecoin output]({baseDir}/references/memecoin-output.md). Build a
review queue from `matches` followed by `other_matches`, preserving their
ranking; review at most ten distinct candidates. Do not expand the sample
or repeat discovery to fill a list. For this recipe, both strong picks and
fallbacks must have `decision: pass`, satisfy the age/cap/social requirements,
and have usable top-20 account share and organic-score evidence. Unknown
or rejected candidates cannot become a fallback merely to produce output.

Compare actual distribution, liquidity, turnover and organic/social evidence.
Top-20 concentration measures token accounts, not independent wallet owners.
Prioritize complete, fresh evidence and account for material authority,
liquidity, tax or other supported concerns. Do not call the best of a poor
sample strong simply because it ranks first. Explain material weaknesses
inside the selected card; do not treat missing evidence as measured weakness.

Apply the [fresh-call procedure]({baseDir}/references/fresh-calls.md) using
`--timezone America/Mexico_City` before final selection. Skip reported mints
and continue through the same ten-candidate queue. A repeated strong token
must not prevent choosing another unreported strong candidate.

Choose one to three unreported strong candidates when supported. Only if
none remain, choose one eligible unreported weaker candidate and state its
known weakness. Do not fill remaining slots with weaker candidates when a
strong pick exists. For final selections only, reuse a matching stored
snapshot or save one exact-mint Jupiter search per pick (at most three
additional HTTP calls, no RPC), then record with `good-call --if-new`.
Follow the fresh-call rules for identity/run matching, concurrent duplicates
and already-recorded selections. Do not exceed the three extra search calls
when replacing a concurrently reported pick. These bookkeeping requests are
separate from the playbook's four discovery HTTP calls. Recording a GoodCall
does not prove external message delivery.

If history is explicitly disabled, skip its checks and writes entirely;
previously reported mints are eligible. Other profile settings remain.

## Output and incomplete runs

- Strong results: one to three token cards, respecting the memecoin format.
- No strong result: one **Weaker candidate** card with its known weakness,
  provided it passed the hard filters and has the required usable evidence.
- No eligible unreported result in the reviewed sample, with sufficient
  evidence to assess it: exactly `No good tokens scanned`.
- If required evidence gaps, failed discovery or exhausted verification
  prevent assessment and there is no eligible result, use
  `Screen incomplete: insufficient evidence to assess candidates.`
  Missing runtime/configuration or call-history failures use their specific
  short failure message. Do not misreport failures as an empty screen.

Usable picks may still be returned from a partial screen; never imply all
feeds or candidates were successfully checked. Missing liquidity that
prevents judging a candidate must not be presented as known weak liquidity.
The normal bounded sample does not itself constitute a provider failure.
Preserve saved picks if a later history operation fails, as instructed by
fresh calls.

Return only results or the one-line status, with condition-appropriate
emojis and at most 3,000 characters. Keep full mints and material evidence;
omit top-holder lists, filenames, commands, budgets, filter recaps and routine
footers. Mention speculation briefly within results. Output may be used on
a channel such as Discord or Telegram.
