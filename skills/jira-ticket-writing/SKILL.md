---
name: jira-ticket-writing
description: "Draft concise Jira tickets from technical discussion, with user-story structure, context-as-tasks, acceptance criteria, DoR, and DoD."
version: 1.2.2
author: François Naturé + Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [jira, tickets, user-stories, french, acceptance-criteria, dor, dod]
---

# Jira Ticket Writing

Use this skill when drafting Jira issue text, titles, user stories, implementation tickets, acceptance criteria, Definition of Ready (DoR), or Definition of Done (DoD) from a technical discussion.

## Core workflow

1. Identify the **actual requested work**, not just the topic.
2. Produce a short **title** first when the user asks for one; otherwise include it with the ticket body.
3. Use the user's requested structure exactly when provided.
4. For François/Bro, prefer **concise French** for Jira tickets unless he asks otherwise.
5. Remove placeholder words such as `remplir`; replace them with concrete content.
6. For François/Bro, write `Titre`, `Je veux`, and `Afin de` in simple, high-level language that non-specialists can understand. Avoid implementation details and low-level technical names in these three sections unless indispensable.
7. Give each user-story section a distinct purpose:
   - `Je veux` states the capability or high-level change being requested. It may mention the solution direction, but not implementation details.
   - `Afin de` states the functional, business, user, or operational outcome—not the technical mechanism. Express the value obtained once the change exists (for example: simpler maintenance, lower operational risk, clearer ownership, greater autonomy).
   - Do not repeat the implementation from `Je veux` inside `Afin de`.
8. Put the technical explanation and concrete **implementation tasks** inside `Contexte`. Keep `Critères d’acceptation` precise, observable, testable, and technically detailed when needed. Always format every acceptance criterion as an unchecked Jira checkbox (`- [ ]`), not as prose or a plain bullet list. When the source already supplies acceptance criteria, preserve their identifiers, priority labels, titles, and wording verbatim: only add checkbox formatting. Never split, merge, expand, reinterpret, rewrite, or supplement supplied acceptance criteria unless the user explicitly asks for that.
9. Add `Definition of Ready (DoR)` and `Definition of Done (DoD)` immediately after `Critères d’acceptation`, in that order. These two sections are invariant standards: reproduce the canonical checklists below verbatim in every complete ticket. Never adapt, expand, shorten, reorder, or specialize their items for the ticket.
10. Apply the following lifecycle rules:
    - The DoR is checked during refinement, before the ticket enters a sprint. If it is not satisfied, the ticket remains `To Refine` rather than being forced into the sprint.
    - The DoD is checked when closing the ticket. Its requirements must not be silently weakened between refinement and closure.
    - These canonical DoR/DoD checklists are the standing team standard supplied by François. Do not substitute project- or ticket-specific variants unless François explicitly provides a new canonical standard.
11. Do not create the Jira issue in Jira unless credentials/project are available or the user explicitly provides the target project/key.
12. For automation tickets, do not hide the mechanism behind vague verbs such as “automate” or “secure.” Name the executor/schedule, APIs or systems crossed, credential propagation/reload behavior, validation gate, overlap or rollback strategy, old-resource retirement rule, and alert conditions. Keep the ticket concise by expressing these as implementation bullets rather than a long design essay.

## Canonical DoR and DoD

The following checklists come from the supplied DoR/DoD reference document and are fixed. Copy them verbatim into every complete ticket. Do not replace them with ticket-specific readiness conditions or technical validation steps.

```markdown
**Definition of Ready (DoR)**

- [ ] Le titre est actionnable et compréhensible sans ouvrir le ticket.
- [ ] Le contexte précise pourquoi le travail est nécessaire et pour qui, en une ou deux phrases.
- [ ] Les critères d’acceptation sont vérifiables.
- [ ] Le ticket est estimé en points ou en jours.
- [ ] Les dépendances, blocages, accès nécessaires et décisions en attente sont identifiés.
- [ ] L’Epic ou l’objectif est identifié pour assurer la traçabilité de la charge et du suivi.
- [ ] Aucune information nécessaire ne manque pour pouvoir démarrer le travail.

**Definition of Done (DoD)**

- [ ] Les critères d’acceptation sont vérifiés un par un.
- [ ] La PR est revue et approuvée par un pair.
- [ ] Pour les travaux de développement uniquement, les tests unitaires sont verts, ainsi que les tests de recette lorsqu’ils sont applicables.
- [ ] La documentation est à jour si un comportement ou une procédure a changé.
- [ ] Le changement est déployé en développement au minimum, et en recette lorsqu’elle est prévue.
- [ ] Aucun effet de bord ni aucune régression connue ne subsiste.
```

For DevOps or infrastructure tickets, keep the unit-test line exactly as written: its `travaux de développement uniquement` qualifier makes it non-applicable without altering the canonical DoD. Likewise, do not remove another item merely because it may ultimately be non-applicable; applicability is assessed when the checklist is completed.

## Preferred French template

```markdown
**Titre**
<action concise + composant>

**Je veux**
<capacité ou changement à mettre en œuvre>

**Afin de**
<bénéfice métier, utilisateur ou opérationnel>

**Contexte**
Les tâches à effectuer sont :

- <tâche 1>
- <tâche 2>
- <tâche 3>

**Critères d’acceptation**

- [ ] <résultat observable>
- [ ] <valeur par défaut ou configuration vérifiée>
- [ ] <validation de rendu, de fonctionnement ou de documentation>

**Definition of Ready (DoR)**

- [ ] Le titre est actionnable et compréhensible sans ouvrir le ticket.
- [ ] Le contexte précise pourquoi le travail est nécessaire et pour qui, en une ou deux phrases.
- [ ] Les critères d’acceptation sont vérifiables.
- [ ] Le ticket est estimé en points ou en jours.
- [ ] Les dépendances, blocages, accès nécessaires et décisions en attente sont identifiés.
- [ ] L’Epic ou l’objectif est identifié pour assurer la traçabilité de la charge et du suivi.
- [ ] Aucune information nécessaire ne manque pour pouvoir démarrer le travail.

**Definition of Done (DoD)**

- [ ] Les critères d’acceptation sont vérifiés un par un.
- [ ] La PR est revue et approuvée par un pair.
- [ ] Pour les travaux de développement uniquement, les tests unitaires sont verts, ainsi que les tests de recette lorsqu’ils sont applicables.
- [ ] La documentation est à jour si un comportement ou une procédure a changé.
- [ ] Le changement est déployé en développement au minimum, et en recette lorsqu’elle est prévue.
- [ ] Aucun effet de bord ni aucune régression connue ne subsiste.
```

## Style rules

- Be compact; no long educational exposition inside the ticket.
- For François/Bro, if he asks for a ticket to be **more concise**, compress it aggressively: one sentence per `Je veux`/`Afin de`, short task bullets, and no rationale repeated across sections. Never shorten or otherwise alter the canonical DoR and DoD blocks.
- Draft the entire ticket in French when requested, including the title and headings; retain established technical terms such as deploy token, ExternalSecret, GitOps and GitLab subgroup.
- Preserve the user's headings if supplied.
- Prefer implementation-oriented wording in `Contexte`.
- Avoid filler and meta-commentary.
- If the user asks for only a title, return only the title; do not append DoR or DoD.
- When the user asks to revise only one section or excerpt (for example, « refais juste le problème actuel »), return only that revised section. Do not repeat the complete ticket or surrounding material.
- Do not invent an estimate, Epic, dependency, environment, deployment result, review, or validation. Mark unknown readiness information explicitly as `À renseigner` or `À confirmer`.
- Supplied acceptance criteria are authoritative source text. Preserve them word for word and only add `- [ ]` checkbox syntax; add or rewrite criteria solely when the user explicitly requests it.
- For François/Bro, do not add an `Informations de suivi` section or any equivalent metadata recap. Jira metadata and links such as priority, responsibility, chapter, `is blocked by`, and `blocks` are managed outside the ticket body unless he explicitly asks to include them. Keep only task-relevant dependency details in `Contexte` when they are necessary to understand or execute the work.
- In the generated ticket, keep DoR and DoD directly after the acceptance criteria even when another section would traditionally follow them.
- Always reproduce the canonical DoR and DoD verbatim. Ticket-specific prerequisites, validations, dependencies, or evidence belong in `Contexte`, the supplied acceptance criteria, or dedicated metadata—not in the DoR or DoD blocks.

## Helm/Kubernetes implementation-ticket pitfall

When drafting a ticket for a Helm chart feature, distinguish **where the resource lives** from what it affects. For example, a `PodDisruptionBudget` should usually be a **separate Helm template**, not embedded in the `Deployment` template. In the context/tasks, call out related default values that must be aligned, such as `replicaCount`, `RollingUpdate` strategy, `rollingUpdate.maxUnavailable`, `rollingUpdate.maxSurge`, and HPA `minReplicas` when relevant.

See `references/helm-pdb-production-ticket.md` for concise ticket notes about PDB support in reusable Helm charts.
