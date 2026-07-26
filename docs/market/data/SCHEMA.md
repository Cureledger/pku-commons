# PKU Market Atlas: dataset schema

Investor- and innovator-facing market data for phenylketonuria (PKU). **No biomedical/mechanism
science.** This is the market: products, money, providers, geography, trials, advocacy, litigation.

Every dataset file is JSON with this envelope:

```json
{
  "dataset": "<slug>",
  "title": "<human title>",
  "updated": "2026-07-26",
  "source_note": "one line on where the data came from and its limits",
  "records": [ /* array of records, shape per dataset below */ ]
}
```

Every record carries provenance:

- `sources`: array of `{ "title": "...", "url": "..." }`, at least one per record where possible.
- `confidence`: `"sourced"` (backed by a citation) | `"estimate"` (reasoned, no single source) |
  `"unknown"` (placeholder, needs a contributor).

Keep values factual. Dollar figures, patient counts, and prices must cite a source or be marked
`estimate`. Never give investment advice. Surface facts and opportunities only.
