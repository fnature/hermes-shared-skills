# OVH Shared Apache: Markdown Representations

Use this adapter only when repository instructions or deployment evidence confirm OVHcloud shared Web Hosting with Apache `.htaccess` support.

## Architecture

Generate HTML and Markdown at build time. Apache selects the representation; it should not convert HTML on every request.

```text
source -> build -> page.html + page.md -> OVH Apache -> representation selection
```

Inspect existing `.htaccess` before editing. Preserve HTTPS enforcement, canonical-host redirects, clean URLs, error handling, PHP/application routing, security headers, and existing MIME/caching rules.

## Conservative example

```apache
AddType text/markdown .md
RewriteEngine On

# Home: negotiated Markdown only when explicitly requested and present.
RewriteCond %{HTTP_ACCEPT} (^|,|;)\s*text/markdown(?:\s*;|\s*,|$) [NC]
RewriteCond %{DOCUMENT_ROOT}/index.md -f
RewriteRule ^$ index.md [L]

# Clean page: negotiated Markdown before HTML fallback.
RewriteCond %{HTTP_ACCEPT} (^|,|;)\s*text/markdown(?:\s*;|\s*,|$) [NC]
RewriteCond %{DOCUMENT_ROOT}/$1.md -f
RewriteRule ^(.+?)/?$ $1.md [L]

RewriteCond %{DOCUMENT_ROOT}/$1.html -f
RewriteRule ^(.+?)/?$ $1.html [L]
```

Adapt to actual routes. Do not blindly paste this over an existing ruleset. Apache may add `Vary: Accept` because the rewrite condition reads `Accept`; verify rather than assume.

## Required live checks

```bash
curl -i https://example.com/about
curl -i -H 'Accept: text/markdown' https://example.com/about
curl -i https://example.com/about.md
```

Confirm respectively:

1. normal HTML and `Content-Type: text/html`;
2. Markdown, `Content-Type: text/markdown; charset=utf-8`, and `Vary: Accept`;
3. explicit Markdown with the correct MIME type.

Test cache/CDN behavior if present. Do not mark negotiation `PASS` from source rules alone.

## Do not introduce unnecessary runtime

Do not add Node.js, PHP routing, a reverse proxy, or another service solely for negotiation when Apache can safely select pre-generated files. Conversely, do not use this adapter on a different hosting stack.
