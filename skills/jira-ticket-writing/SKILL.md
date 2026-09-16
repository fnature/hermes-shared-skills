---
name: jira-ticket-writing
description: "Draft concise Jira tickets from technical discussion, with user-story structure, context-as-tasks, and acceptance criteria."
version: 1.0.0
author: François Naturé + Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [jira, tickets, user-stories, french, acceptance-criteria]
---

# Jira Ticket Writing

Use this skill when drafting Jira issue text, titles, user stories, implementation tickets, or acceptance criteria from a technical discussion.

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
8. Put the technical explanation and concrete **implementation tasks** inside `Contexte`. Keep `Critères d’acceptation` precise, testable, and technically detailed when needed.
9. Do not create the Jira issue in Jira unless credentials/project are available or the user explicitly provides the target project/key.
10. For automation tickets, do not hide the mechanism behind vague verbs such as “automate” or “secure.” Name the executor/schedule, APIs or systems crossed, credential propagation/reload behavior, validation gate, overlap or rollback strategy, old-resource retirement rule, and alert conditions. Keep the ticket concise by expressing these as implementation bullets rather than a long design essay.

## Preferred French template

```markdown
**Titre**
<action concise + component>

**Je veux**
<capability/change to implement>

**Afin de**
<business/operational benefit>

**Contexte**
Les tâches à effectuer sont :

- <task 1>
- <task 2>
- <task 3>

**Critères d’acceptation**

- <observable result>
- <default/config value verified>
- <render/test/doc validation>
```

## Style rules

- Be compact; no long educational exposition inside the ticket.
- For François/Bro, if he asks for a ticket to be **more concise**, compress it aggressively: one sentence per `Je veux`/`Afin de`, short task bullets, and no rationale repeated across sections.
- Draft the entire ticket in French when requested, including the title and headings; retain established technical terms such as deploy token, ExternalSecret, GitOps and GitLab subgroup.
- Preserve the user's headings if supplied.
- Prefer implementation-oriented wording in `Contexte`.
- Avoid filler and meta-commentary.
- If the user asks for only a title, return only the title.
- When the user asks to revise only one section or excerpt (for example, « refais juste le problème actuel »), return only that revised section. Do not repeat the complete ticket or surrounding material.

## Helm/Kubernetes implementation-ticket pitfall

When drafting a ticket for a Helm chart feature, distinguish **where the resource lives** from what it affects. For example, a `PodDisruptionBudget` should usually be a **separate Helm template**, not embedded in the `Deployment` template. In the context/tasks, call out related default values that must be aligned, such as `replicaCount`, `RollingUpdate` strategy, `rollingUpdate.maxUnavailable`, `rollingUpdate.maxSurge`, and HPA `minReplicas` when relevant.

See `references/helm-pdb-production-ticket.md` for concise ticket notes about PDB support in reusable Helm charts.
