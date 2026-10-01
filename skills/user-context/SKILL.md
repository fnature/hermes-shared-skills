---
name: user-context
description: "Use when conversation or a request contains or depends on the current user's private work or life context: identity, mission, relationships, preferences, initiatives, decisions, blockers, plans, or meaningful changes. Retrieve the minimum relevant active-profile notes, proactively preserve durable context even without the phrase 'remember this', organize topic notes dynamically under stable work/life roots, verify volatile facts from authoritative sources, and report every durable update."
version: 1.2.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [user-context, work-memory, life-memory, private-memory, profile-scoped]
    related_skills: [agent-memory-architecture]
---

# User Context

## Purpose

This shared skill defines how to retrieve, curate, and reorganize private user context without storing that private material in a Git repository or inside the skill itself.

The private store has two stable roots and dynamic topic notes beneath them:

```text
<active-profile-home>/
└── custom-memory/
    ├── work-memory/
    │   ├── _index.md
    │   ├── profile-and-mission.md
    │   ├── current-focus.md
    │   ├── projects/
    │   ├── organisation/
    │   ├── working-methods/
    │   └── archive/
    └── life-memory/
        ├── _index.md
        ├── profile.md
        ├── current-focus.md          # create only when useful
        ├── personal-projects/
        ├── relationships/
        ├── interests/
        ├── plans/
        └── archive/
```

Only the roots and their `_index.md` files are structural invariants. Do not pre-create empty categories merely because this example lists them. Let recurring content earn a note or subdirectory.

The skill is generic: it must not contain a particular user's name, employer, family details, projects, or other dossier content.

## Resolve the active profile home

Use the active Hermes profile identified by the runtime context.

- For the default profile, the profile home is `~/.hermes/`.
- For a named profile, it is `~/.hermes/profiles/<active-profile>/`.

Always read and write context under the **active profile home**. Do not silently fall back to the default profile or another named profile when files are missing. Report the missing context instead.

Only inspect or update another profile's context when the user explicitly requests a cross-profile operation.

## Retrieval workflow

1. **Classify scope.** Decide whether the request is `work`, `life`, `both`, or `neither`. Do not load life context merely because a work request names the user, and do not load work context for an unrelated personal request.
2. **Resolve the active profile.** Use only its private context roots.
3. **Read the relevant index first.** Inspect `custom-memory/work-memory/_index.md`, `custom-memory/life-memory/_index.md`, or both. Use listed aliases, relationships, status, and canonical paths to select likely notes.
4. **Search when routing is uncertain.** Search filenames and note content for the user's words plus likely aliases or concepts. Prefer exact search for names, IDs, projects, error codes, and acronyms; use semantic retrieval when a connected source such as Joplin provides it. Some file-search backends omit content below hidden parent directories such as `.hermes`; if a search unexpectedly returns no matches, do not infer absence—follow index paths and read likely notes directly.
5. **Load minimally.** Read only the smallest useful set of notes or sections. Stable identity, mission, and enduring preferences belong in `profile-and-mission.md` or `profile.md`; dated priorities belong in `current-focus.md`; developed subjects belong in focused topic notes.
6. **Recover evidence when needed.** For a claim about a prior conversation or decision, use `session_search` and inspect the source session. Curated notes are synthesis; sessions preserve conversational evidence.
7. **Prefer direct current sources.** If the user provides a repository, issue, document, Joplin note, calendar, cluster, file, account, or URL, inspect that source before treating a stored summary as current proof.
8. **Label epistemic state.** Keep established facts, dated state, user-attributed reports, model synthesis, and uncertainty distinguishable. Never silently turn stale state or inference into present fact.

Retrieval is complete when the answer uses the minimum relevant context and every volatile claim is either dated, qualified, or checked against an authoritative current source.

## Proactive capture policy

During ordinary work or life conversation, identify durable context worth retaining even when the user does not explicitly say "remember this." A statement is a good memory candidate when it is likely to improve future understanding or materially change future advice, including:

- stable identity, role, mission, relationship, preference, or constraint;
- a meaningful project, personal plan, responsibility, or recurring subject;
- an accepted decision and its rationale;
- a durable correction to stored context;
- a significant change in ownership, status, hierarchy, or relationship;
- an ongoing blocker, unresolved question, or commitment likely to matter later;
- vocabulary, architecture, or background repeatedly needed to understand the user's world.

Do not durably capture by default:

- casual small talk or every passing mood;
- routine task progress and short-lived status;
- raw conversation transcripts or long quotations;
- temporary errors already recoverable from the source session;
- facts better obtained from a current repository, Jira, calendar, cluster, or other live source;
- speculative interpretations presented as facts;
- secrets, tokens, keys, certificate or keystore contents, financial account data, or medical records.

Sensitive information about colleagues, family, health, finances, personnel matters, or private relationships needs stricter minimization. Preserve it only when the user clearly wants continuity and the future value outweighs the privacy cost; ask before recording unusually sensitive material.

## Maintenance workflow

When durable context is identified:

1. **Retrieve before writing.** Read the relevant index and canonical note so new material is reconciled rather than blindly appended.
2. **Classify the record.** Distinguish `fact`, `event`, `decision`, `preference`, `constraint`, `question`, `plan`, or `temporary state`.
3. **Choose the smallest canonical home.** Update an existing note when it already owns the subject. Create a focused note only when the subject has durable independent value.
4. **Record time and provenance.** Date volatile information; preserve a source session, note, repository, document, or explicit user attribution when useful.
5. **Reconcile change.** Replace a simple corrected fact. When chronology or rationale matters, mark the prior statement `superseded` and link the replacement instead of silently erasing history.
6. **Maintain discoverability.** Update the root `_index.md` whenever a canonical note is created, renamed, moved, archived, or gains a useful alias or relationship.
7. **Verify the write.** Re-read changed material, check links/paths, and ensure work/life boundaries remain intact.
8. **Report the update.** Tell the user which active-profile files and sections were created, updated, moved, or archived. If no durable update was warranted, do not pretend one occurred.

For changing initiatives, prefer:

```markdown
## Initiative name

- **Status:** active | blocked | planned | completed | superseded | to confirm
- **Last updated:** YYYY-MM-DD
- **Context:** why it exists
- **Current decision:** accepted direction, if any
- **Blocker / next step:** what constrains progress
- **Provenance:** source session, note, repository, document, or user statement
```

For changing life information, include dates only when chronology or freshness matters.

## Dynamic organization policy

Use **stable roots, dynamic leaves**. The assistant may evolve files and subdirectories as the user's world develops, but it must preserve predictable routing and reversible history.

### When a subject earns its own note

Create a focused note when at least one condition holds:

- it has several durable facts or multiple dated updates;
- it is likely to be retrieved independently;
- it has its own decisions, blockers, people, chronology, or source references;
- keeping it in a broader note obscures that note's purpose;
- it crosses the practical size or complexity threshold where targeted retrieval is clearly better.

Keep a subject as a section when it is small, stable, and normally retrieved with its parent topic. Do not create one file per fact.

### Splitting, merging, moving, and archiving

- **Split** a note when it mixes independent retrieval subjects or has become cumbersome to update safely.
- **Merge** notes when they overlap heavily and neither has an independent retrieval purpose.
- **Move** a note only when its canonical category is clearly wrong or the index can no longer route to it cleanly.
- **Archive** completed or obsolete context when historical value remains. Prefer archiving or marking `superseded` over deletion.
- Leave a short compatibility pointer at an old well-known path when removing it would break established retrieval or references.
- Update inbound index links and aliases in the same operation.
- Avoid repeated taxonomy churn. A merely prettier hierarchy is not sufficient reason to reorganize.

### Index contract

Each root `_index.md` should remain concise and contain:

- the root's scope and authority;
- canonical note paths grouped by useful subject;
- aliases/acronyms that aid routing;
- status where it affects retrieval (`active`, `historical`, `to confirm`);
- notable relationships between notes;
- last structural review date;
- an explicit pointer to `archive/` when it exists.

The index is a map, not a duplicate knowledge base.

## Autonomy boundaries

### May perform automatically and report afterwards

- update an existing non-sensitive canonical note;
- add or revise a section, timestamp, provenance item, alias, or index entry;
- create a focused note under an established category;
- mark an outdated statement superseded;
- archive completed material without deleting it;
- make a small split or merge that has one obvious canonical result.

### May perform when useful, but must explicitly highlight it

- create a new project or life-topic subdirectory;
- split or merge a substantial note;
- move context between work and life roots;
- change which note is canonical;
- record context about another identifiable person.

### Ask before acting

- delete durable context or erase historical provenance;
- perform a broad reorganization affecting many notes;
- record unusually sensitive personal, medical, financial, family, personnel, or relationship information;
- expose private context to an external service, provider, model, delegated agent, or integration;
- change the declared source-of-truth hierarchy.

An explicit user request may authorize a bounded large reorganization. It does not authorize unrelated deletion or external exposure.

## Periodic consolidation

Do not reorganize after every conversation. Consolidate when there is evidence of drift:

- an index no longer routes cleanly;
- a note mixes several independently retrieved subjects;
- duplicate or contradictory facts appear;
- an active subject has become historical;
- aliases and links no longer reflect the user's vocabulary;
- a source-of-truth transition, such as Joplin integration, requires reconciliation.

A consolidation pass should inventory the affected root, propose or execute the smallest reversible structure change allowed by the autonomy policy, preserve provenance, update indexes, and report every structural change.

## Cross-profile policy

Profiles are isolated stores, even when they currently contain identical copies.

- Update only the active profile by default.
- Do not assume a correction made in one profile exists in another.
- Synchronize multiple profiles only when explicitly requested.
- Before cross-profile synchronization, compare files and preserve newer or profile-specific information rather than blindly overwriting it.
- Keep context directories at `0700` and files at `0600` where supported.

## Privacy and external exposure

- Never copy private context into a Git repository.
- Never publish, email, post, or send it to an external service without explicit instruction.
- Use the minimum relevant excerpt in answers and tool calls.
- Do not pass entire context files to delegated agents when a narrow summary is sufficient.
- State when an external model, memory provider, or integration would receive personal or professional context if that exposure is not already obvious.

## Joplin integration target

Joplin is intended to become the human-reviewed source of truth when connected.

After integration:

- Joplin should hold authoritative reviewed notes;
- this skill should retain capture, retrieval, reconciliation, and maintenance rules;
- profile-local files may remain as clearly labeled caches, routing indexes, or fallback summaries;
- cache files should record their synchronization date and corresponding Joplin note identifier;
- conflicts must be reported, with the current Joplin note preferred after freshness is confirmed;
- avoid two unlabeled authoritative copies;
- use keyword search for names, IDs, acronyms, and exact errors, and semantic search for concepts or paraphrases.

## Common pitfalls

- Reading another profile because the active profile lacks context.
- Loading both work and life dossiers for every request.
- Treating a dated context note as live infrastructure or calendar state.
- Appending without retrieving and reconciling the existing note.
- Creating one file per fact or retaining one giant file for unrelated subjects.
- Reorganizing repeatedly for aesthetic reasons and breaking canonical paths.
- Failing to update `_index.md` after structural changes.
- Concluding that context is absent from an empty content-search result when the profile store sits below a hidden `.hermes` directory; use the index and direct reads as the fallback.
- Mixing family/private-life material into professional project notes.
- Duplicating detailed context into tiny always-loaded memory.
- Committing profile-local context to a shared repository.
- Hiding uncertainty, contradiction, or provenance behind a polished summary.
- Silently building an extensive dossier on third parties.
- Letting future Joplin notes and local caches diverge without a declared authority hierarchy.

## Verification checklist

- [ ] The active profile home was resolved correctly.
- [ ] The request or conversation was classified as work, life, both, or neither.
- [ ] The relevant root index was read before topic notes were selected or modified.
- [ ] Only the minimum relevant private context was loaded or exposed.
- [ ] New durable context passed the capture policy; transient detail was not promoted.
- [ ] New information was reconciled with the existing canonical note.
- [ ] Volatile claims are dated or verified from a current authoritative source.
- [ ] Facts, attributed reports, inferences, and uncertainties remain distinguishable.
- [ ] Every structural change preserved or updated index routing and provenance.
- [ ] No deletion, broad reorganization, cross-profile access, or external exposure occurred without appropriate authorization.
- [ ] Context directories/files retain restrictive permissions where supported.
- [ ] Any update was reported with its active-profile path and section.
