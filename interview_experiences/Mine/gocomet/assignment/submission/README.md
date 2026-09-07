# FreightLens Design Exercise — Submission

**Candidate:** Harsha Vardhan Raja  
**Date:** August 2026

## What's in this folder

```
submission/
├── FreightLens_Design_Document.html   ← Main design document (open in Chrome)
└── README.md                          ← This file
```

## How to generate the PDF

1. Open `FreightLens_Design_Document.html` in **Google Chrome**
2. Press `Cmd + P` (Print)
3. Set **Destination** to "Save as PDF"
4. Set **Margins** to "Default"
5. Enable "Background graphics"
6. Click **Save**

All 4 architecture diagrams are embedded inline — no separate image files needed.

## Document Structure (5 pillars as required)

| Section | Content | Est. pages |
|---------|---------|-----------|
| 1. Data Organization Design | Medallion Architecture, ingestion paths, stage breakdown, schema sketches, justification | ~2 |
| 2. Access Architecture | Participant access map, tenant isolation, dedicated DB coexistence, NL→SQL pipeline | ~2 |
| 3. End-to-End Trace | Full step-by-step walkthrough of the delayed ETD rebid scenario | ~1.5 |
| 4. Failure Analysis | 2 silent failure modes with root cause, impact, and mitigation | ~1.5 |
| 5. Tradeoffs | 3 deliberate omissions, 3x scale bottleneck, self-critical assessment | ~1 |

## Diagrams (embedded in HTML)

- **Figure 1:** Data Organization Architecture — Medallion Pattern on ClickHouse
- **Figure 2:** Connection Router — Dedicated DB Coexistence Model
- **Figure 3:** NL → SQL Safety Pipeline — 4 Validation Gates
- **Figure 4:** End-to-End Sequence — Delayed ETD & Rebid Evaluation (in the trace section)

