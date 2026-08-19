# Readiness Audit Report

Report evidence, not ceremonial checkboxes.

## Summary

State the inspected source/public root, build command and result, impact mode, confirmed domain/hosting, and whether live/browser/manual checks ran.

## Findings

Group findings by priority and include file/URL evidence:

### Critical / P0

Broken operation, inaccessible essential interaction, uncrawlable content, broken links, invalid primary semantics, privacy exposure, or factual fabrication.

### SEO / P1

Content, metadata, headings, links, canonicals, redirects, robots, sitemap, structured data, provenance, and performance.

### Accessibility and UX

Keyboard, focus, contrast, images, forms, landmarks, menus, motion, responsive behavior, and screen-reader findings.

### AI/Agent Readiness / P2

| Capability | Status | Evidence/reason |
|---|---|---|
| Extractable canonical HTML | PASS/FAIL/BLOCKED | |
| Markdown alternates | PASS/FAIL/BLOCKED/N/A | |
| `text/markdown` | PASS/FAIL/BLOCKED/N/A | |
| `Accept: text/markdown` | PASS/FAIL/BLOCKED/N/A | |
| `Vary: Accept` | PASS/FAIL/BLOCKED/N/A | |
| Markdown `rel="alternate"` | PASS/FAIL/BLOCKED/N/A | |
| `llms.txt` | PASS/FAIL/BLOCKED/N/A | |
| `llms-full.txt` | PASS/FAIL/BLOCKED/N/A | |
| Agent-actionable controls/forms | PASS/FAIL/BLOCKED/N/A | |

### External authority / P3

List legitimate actions outside the codebase. Never label them implemented without external evidence.

## Recommended actions

Order actions by P0, P1, P2, then P3. Separate code changes from facts the owner must provide and checks that require deployment/manual review.

## Completion language

- `PASS` requires observed evidence.
- `FAIL` names the exact correction.
- `BLOCKED` names the missing fact/environment/test.
- `N/A` states why implementation would add no value or create maintenance risk.
