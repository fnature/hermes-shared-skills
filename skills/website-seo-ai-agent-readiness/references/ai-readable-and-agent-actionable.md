# AI-Readable and Agent-Actionable Websites

## Canonical HTML first

A crawler or text extractor should understand each important page from its HTML without executing the full frontend application. AI-specific artifacts supplement this foundation.

## Markdown alternates

Consider an explicit `.md` representation for important informational pages when it can be generated from the same source as HTML. Preserve headings, paragraphs, lists, tables, links, code, and useful image descriptions; remove navigation duplication, banners, decorative UI, tracking, and layout boilerplate.

Serve explicit Markdown as:

```http
Content-Type: text/markdown; charset=utf-8
Link: <https://example.com/page>; rel="canonical"
```

Advertise it from HTML when present:

```html
<link rel="alternate" type="text/markdown" href="https://example.com/page.md">
```

Do not list a mere Markdown alternate as a separate canonical sitemap URL.

## Content negotiation

`Accept: text/markdown` is optional. Implement it only when the hosting stack supports correct representation selection and cache behavior. HTML remains the default for `Accept: text/html`, absent headers, and normally `*/*`. Never identify “AI” solely by `User-Agent`.

When one URL serves multiple representations, verify:

```http
Vary: Accept
```

Also keep explicit `.md` URLs available when useful. Test HTML, negotiated Markdown, and explicit Markdown separately on the deployed server.

## llms.txt

A concise root-level `llms.txt` may identify the site, describe it factually, and link to authoritative HTML or Markdown resources. It is an emerging convention, not a ranking or citation guarantee.

`llms-full.txt` is optional and suitable only when a bounded, useful consolidation can stay synchronized. Do not blindly concatenate archives, boilerplate, drafts, excluded pages, sensitive data, or content too large to be practical.

## Agent-actionable interaction

For actions intended to be usable by people or automation:

- use native links and controls with explicit names;
- provide predictable labels, constraints, validation, and errors;
- expose stable action destinations and meaningful success states;
- keep essential actions independent of hover or animation;
- confirm consequential or irreversible actions;
- respect authentication and authorization boundaries;
- document APIs/contracts when programmatic action is intentionally supported;
- use idempotency for safely repeatable API operations where applicable;
- avoid CAPTCHA as the only critical path when a safer accessible alternative exists.

Do not invent automation capabilities. A readable brochure site need not expose an API; a contact form merely needs clear, accessible, safe behavior.

## Decision states

Use:

- `PASS`: implemented and verified.
- `FAIL`: applicable but wrong or broken.
- `BLOCKED`: applicable but needs facts, hosting, permission, or live/manual tests.
- `N/A`: not beneficial or intentionally unsupported, with a reason.

Missing optional Markdown or LLM files is not automatically failure.
