# Discovery commands and scope

Use the installed `growr` executable described in SKILL.md. Global flags
such as `--json`, `--max-http-calls`, and `--max-rpc-calls` precede the command.
These examples show only the arguments after `growr`.

| Intent | Arguments |
| --- | --- |
| Jupiter name/symbol | `--json search jupiter JUP` |
| Jupiter exact mint | `--json search jupiter MINT` |
| Stonkfun text | `--json search stonks te --sort volume --page 1 --page-size 30` |
| Jupiter recent pools | `--json list jupiter` |
| Ranked Jupiter feed | `--json list jupiter --jupiter-search toptraded --interval 1h --limit 20` |
| Stonkfun newest | `--json list stonks --stonk-search recent` |
| Stonkfun category | `--json list stonks --stonk-search volume --category xstock --page-size 30` |

Jupiter ranked modes: `toptraded`, `toptrending`, `toporganicscore`. They accept
intervals 5m/1h/6h/24h and limits 1-100. Its recent mode accepts neither flag.
Recent refers to first pool creation, not a verified mint-creation timestamp.
Jupiter query search accepts no feed, page, category, interval or sort flags.

Stonkfun listing modes: `recent`, `marketCap`, `volume`. All support page,
page-size (1-100), and quote category. Categories: xstock, prestock, custom,
collectibles, currencies, leverage. Query search accepts sort
marketCap/volume/newest and pagination, but not category or `--on-chain`.

Jupiter lists/searches cost one provider HTTP request. Stonkfun search costs
one; list costs one plus optional Jupiter enrichment batches, normally one
additional batch per nonempty page. Both ordinary discovery modes use no RPC.

Read `records[].identity.mint`, source-attributed `metrics`, `social`, and
`coverage`; `pagination` is provider scope, not proof of an exhaustive search.
Never sum token-level Jupiter liquidity across pool records. Missing metrics
remain unknown. A provider's organic score, verification flag, or social link
does not establish safety or identity.

Supported contracts: CLI schema 2.2, discoverable with `growr schema`.
