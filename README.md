# Hermes Shared Skills

Canonical, version-controlled skills shared by every local Hermes profile through `skills.external_dirs`.

## Shared directory

```text
/workspace/dev/hermes-shared-skills/skills
```

Every profile config should contain:

```yaml
skills:
  external_dirs:
    - /workspace/dev/hermes-shared-skills/skills
```

Local profile skills take precedence over shared skills with the same name. Do not create a profile-local copy of a shared skill unless an intentional override is required.

## Website workflow

The `website-seo-ai-agent-readiness` skill complements `frontend-design`:

- `frontend-design`: visual direction, layout, interaction, public copy, and visual QA.
- `website-seo-ai-agent-readiness`: semantic delivery, SEO, accessibility, performance, machine-readable representations, and release verification.

Use `/website-build` when explicitly invoking both together. Natural-language website work should also trigger the readiness skill from its description.

## Audit tool

```bash
python3 skills/website-seo-ai-agent-readiness/scripts/audit_static_site.py /path/to/public-root
```

For release checks with a confirmed public URL:

```bash
python3 skills/website-seo-ai-agent-readiness/scripts/audit_static_site.py \
  /path/to/public-root \
  --base-url https://example.com \
  --production
```

The tool exits non-zero only for `FAIL` findings. `BLOCKED` items require facts or a live environment; `N/A` items are intentionally optional.
