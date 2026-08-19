# Content, Semantics, and Technical SEO

## Content

Every important page should answer a clear visitor intent with original, specific, current information. Remove filler, keyword stuffing, and needless repetition. Make identity, authorship, evidence, scope, and update dates clear where relevant. Never generate low-value text solely for crawlers.

## Server-visible semantics

Essential text, headings, navigation, links, and form controls should exist in the server response whenever practical. Prefer `header`, `nav`, `main`, `article`, `section`, `aside`, `footer`, headings, paragraphs, lists, tables, `figure`, and `figcaption`. Use `div`/`span` when no semantic element fits.

Use real links for navigation and buttons for actions. Do not require JavaScript to reveal the page’s essential meaning.

## Per-page checks

- One descriptive, unique `<title>`.
- A concise, useful meta description for indexable pages.
- One clear primary `<h1>` and logical heading levels based on structure, not styling.
- Descriptive internal links that make important pages reachable.
- `<meta name="viewport" content="width=device-width, initial-scale=1">`.
- A stable preferred public URL and absolute canonical after the domain is confirmed.
- Redirect permanent duplicate forms only when equivalence is certain; do not erase meaningful query semantics.
- Open Graph/social metadata when the project benefits from sharing previews.

## robots.txt

Provide an intentional root-level policy on production sites. Confirm public content is not accidentally blocked. Reference the sitemap when one exists. Remember:

- crawler names and purposes differ;
- blocking one bot does not block all AI systems;
- model training, retrieval, search indexing, archives, and abusive traffic are distinct policies;
- `robots.txt` is public and cannot secure private paths.

## Sitemap

List canonical, indexable HTML URLs only. Exclude alternates, redirects, errors, drafts, private pages, and `noindex` pages. Do not list both HTML and Markdown when Markdown is an alternate representation. Add `lastmod` only when derived from trustworthy modification data.

## Structured data

Prefer JSON-LD and select types that accurately describe visible content: `WebSite`, `WebPage`, `Article`, `BlogPosting`, `Person`, `Organization`, `BreadcrumbList`, `Product`, `SoftwareApplication`, or `Event` as applicable.

Validate syntax and meaning. Never fabricate identities, qualifications, ratings, reviews, prices, availability, authors, organizations, events, or claims. Structured data is descriptive, not a keyword reservoir.

## External authority

Report legitimate opportunities—professional profiles, repositories, partners, publications, directories, conferences, interviews, citations, and community contributions—as work outside the codebase. Never recommend link farms, paid manipulation networks, fake reviews, fake mentions, or comment spam.
