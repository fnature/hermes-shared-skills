---
name: website-seo-ai-agent-readiness
description: Use whenever creating, updating, reviewing, refactoring, auditing, or preparing a website for deployment. Apply change-scoped requirements for content quality, semantic server-visible HTML, technical SEO, accessibility, performance, structured data, and optional AI/agent-readable representations.
version: 1.0.0
author: François Naturé + Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [website, seo, accessibility, performance, ai-readiness, agents]
    related_skills: [frontend-design, dogfood, website-preview-server]
---

# Website SEO & AI-Agent Readiness

## Overview

Make websites excellent for humans first, then easy for search engines, assistive technology, crawlers, AI retrieval systems, and autonomous agents to understand or use. Canonical, human-readable HTML is the primary representation. Markdown and AI-specific files are additive interoperability layers, never substitutes for sound content and HTML.

Apply this skill automatically to production website work. Pair it with `frontend-design` when visual design, layout, interaction, or public-facing copy changes. Preserve approved design and project behavior while improving machine discoverability.

## When to Use

Use for:

- new websites and production pages;
- changes to public content, navigation, templates, routes, domains, metadata, forms, or deployment;
- SEO, accessibility, performance, structured-data, crawlability, or AI-readiness audits;
- pre-release and post-deployment verification.

Do not run a gratuitous full-site overhaul for a tiny visual correction. Scale checks to the blast radius.

## Priority Ladder

### P0 — Human and crawlable foundation

1. Accurate, useful, original content.
2. Semantic, server-visible HTML and real links/forms.
3. Unique titles, useful descriptions, logical headings, and internal links.
4. Accessibility: keyboard operation, labels, alt text, contrast, landmarks.
5. Responsive, lightweight, performant delivery.
6. Stable URLs and correct canonicalization.

### P1 — Discovery and interpretation

7. Intentional indexability and crawler policy.
8. Correct `robots.txt` and canonical-page sitemap where applicable.
9. Truthful structured data matching visible content.
10. Clear provenance, authorship, dates, and social metadata where useful.

### P2 — AI/agent interoperability

11. Clean extraction from canonical HTML.
12. Generated Markdown alternatives where maintainable.
13. Correct `text/markdown`, canonical/alternate relations, and optionally `Accept: text/markdown` with cache-safe `Vary: Accept`.
14. Concise `llms.txt`; optional, bounded `llms-full.txt`.
15. Predictable forms, validation, success/error states, and safe action semantics.

### P3 — External authority

16. Legitimate citations, profiles, publications, directories, repositories, and earned backlinks. Report these as external actions; never pretend source-code changes created authority.

Never prioritize AI files above broken content, HTML, navigation, accessibility, performance, or canonical URLs.

## Change-Impact Modes

| Mode | Trigger | Required scope |
|---|---|---|
| Concept | Throwaway visual concept or prototype | Content, semantics, headings, links, alt text, responsive and keyboard baseline. No production URLs/files without facts. |
| Narrow | CSS, spacing, colour, crop, or isolated component change | Affected rendering, responsiveness, contrast, focus, semantics, and interaction only. |
| Page/content | New or changed page, article, biography, or service | Affected content, metadata, headings, links, canonical, sitemap, structured data and generated alternates if supported. |
| Site-wide | Navigation, template, routing, domain, deployment, or shared component change | Crawl every affected page; verify links, URLs, directives, metadata, representations, and redirects. |
| Release | Production preparation or explicit full audit | Complete source, build, browser, performance, accessibility, crawl, machine-readable, and deployed HTTP verification. |

If uncertain, choose the smallest mode that covers every changed dependency. A new page is never merely a narrow edit.

## Workflow

### 1. Discover before editing

Determine and record:

- repository instructions (`AGENTS.md`, README, project skills);
- production/public root and source of truth;
- framework/build command and static versus dynamic rendering;
- hosting architecture and existing redirects/rewrite rules;
- canonical domain and URL policy, if confirmed;
- indexable versus private/draft pages;
- existing SEO, accessibility, Markdown, and AI artifacts;
- unresolved facts that block truthful metadata.

Do not infer a canonical domain, identity, credentials, address, price, rating, review, policy, or publication fact.

### 2. Select impact mode

State the scope internally and audit all dependencies it implies. Preserve existing URLs and behavior unless a change is explicitly required.

### 3. Build human-first foundations

Apply the P0 and applicable P1 requirements. Load `references/content-semantics-seo.md` for page foundations and `references/accessibility-performance.md` for interaction and delivery checks.

### 4. Decide AI features, do not cargo-cult them

For each AI feature, choose `PASS`, `FAIL`, `BLOCKED`, or `N/A` with a reason. Use `references/ai-readable-and-agent-actionable.md`.

Generate HTML and Markdown from one source where practical. Never hand-maintain duplicative representations merely to tick a box. Never expose private, draft, excluded, or unverified information through Markdown or LLM files.

### 5. Adapt to actual hosting

Inspect the deployment target. For OVH shared Apache sites, load `references/ovh-apache-markdown.md`. Do not apply Apache rules to nginx, Vercel, Netlify, GitHub Pages, Kubernetes, or application routers.

### 6. Verify with evidence

Run the project’s build/tests, then the shared static audit when applicable:

```bash
python3 /workspace/dev/hermes-shared-skills/skills/website-seo-ai-agent-readiness/scripts/audit_static_site.py PUBLIC_ROOT
```

For release with a confirmed domain:

```bash
python3 /workspace/dev/hermes-shared-skills/skills/website-seo-ai-agent-readiness/scripts/audit_static_site.py \
  PUBLIC_ROOT --base-url https://example.com --production
```

Also perform browser-based desktop/mobile QA for rendered changes. Release mode additionally requires keyboard, contrast, live headers/redirects, performance, and representative screen-reader checks. A source audit cannot prove live server behavior.

### 7. Report honestly

Use four states:

- `PASS` — verified by source, build, browser, or live response.
- `FAIL` — incorrect and actionable.
- `BLOCKED` — requires an unresolved fact, permission, deployment, or manual/live test.
- `N/A` — intentionally inapplicable or not beneficial.

Follow `references/audit-report-format.md`. Do not convert blocked facts into invented values.

## Core Invariants

- `robots.txt` is crawler guidance, not access control.
- Canonical HTML remains dependable and useful without JavaScript whenever practical.
- Real `<a href>`, `<button>`, and native form controls beat click-only containers and gratuitous ARIA.
- Structured data must be valid, truthful, and reflected in visible content.
- Sitemap URLs are canonical and indexable; use truthful `lastmod` only from reliable data.
- AI and HTML representations share publication, privacy, and factual boundaries.
- `llms.txt`, Markdown, and content negotiation do not guarantee rankings, indexing, citations, or agent adoption.
- Never use deceptive cloaking or materially different facts for agents and humans.
- Never create spam backlinks, fake reviews, fake ratings, fake authorship, or fabricated citations.

## Common Pitfalls

1. **Scope explosion:** treat a colour tweak as a narrow mode, not permission to rebuild metadata.
2. **Checkbox theatre:** require evidence and state `BLOCKED`/`N/A`; unchecked does not always mean broken.
3. **Unknown-domain fiction:** defer absolute canonicals, sitemap hostnames, and identity JSON-LD until confirmed.
4. **Representation drift:** generate alternates from a shared source or do not add them.
5. **Cache poisoning:** negotiated responses require correct content types and `Vary: Accept`, verified live.
6. **Rewrite collisions:** inspect existing redirects, HTTPS/canonical-host rules, error handling, and routing before touching `.htaccess`.
7. **Privacy leakage:** never aggregate excluded or sensitive content into `llms-full.txt`.
8. **False completion:** source inspection alone does not prove mobile rendering, assistive use, performance, or deployed headers.

## Definition of Done

The requested change is complete only when:

- the chosen impact mode covers every changed dependency;
- content and server-visible HTML remain useful to humans;
- affected semantics, titles/headings, links, accessibility, responsiveness, performance, and URLs are verified;
- applicable discovery and structured-data artifacts are valid and synchronized;
- AI/agent features have explicit `PASS`/`FAIL`/`BLOCKED`/`N/A` decisions;
- build/tests and the static audit have run successfully where applicable;
- rendered desktop/mobile behavior is checked for user-visible changes;
- live-only and manual checks are reported as blocked until performed;
- no unverified fact or private content was invented or exposed.
