---
name: architecture-adr
description: Read a software requirements document (CDC, user stories, brief), propose and compare three architectures, discuss their trade-offs with the user, pick one, and write an Architecture Decision Record (ADR). Use when asked to design, compare or choose an architecture for a described system, or to write or revise an ADR from such a discussion. Keeps running session notes.
---

# Architecture comparison and ADR

This skill covers two phases that are often run as separate sessions:

- **Phase 1 – Discussion:** read the requirements, propose three architectures, answer the user's follow-up questions, compare them and recommend one.
- **Phase 2 – ADR:** turn the discussion into an ADR and revise it after each round of feedback.

Work out from the request which phase is wanted. If the user gives notes from an earlier discussion, start at Phase 2. If only requirements are given and an ADR is asked for, run Phase 1 briefly yourself (summary, three options, table, decision) and write it into the notes before drafting the ADR.

The rules in "Quality rules" below come from real sessions in which the user had to ask for each of them. Apply them from the first version, not after being asked.

## Notes are mandatory

Keep a notes file for the whole session and update it after **every** step and every answer, not only at the end. Start from `templates/notes_template.md`.

- Phase 1 file (e.g. `Task1_notes.md` or `notes.md`): system summary, functional areas with story numbers, quality attributes, gaps in the requirements, the three architectures, a discussion log with one section per question (`Q1 – …`), the comparison table and the recommendation.
- Phase 2 file (e.g. `task2_notes.md`): inputs used, a short summary of version 1, and a change log. Each change gets **Asked / Why / Done**. Also log changes you made on your own initiative (for example a gap found while drawing a diagram).
- When you correct an earlier statement, say so in the notes ("the earlier note claiming X was overstated") instead of silently replacing it.
- The notes do not need to be a transcript, but everything important from the discussion must be there, including diagrams in plain-text form.

Use the file names the user asks for. If none are given, use the ones above.

## Phase 1 – Discussion

1. **Read the requirements fully.** Number or reuse the story numbers. Build a table that maps every story to a functional area. Check that no story is missing and none is counted twice.
2. **Summarise** what the system does, the roles, and the key quality attributes (security, consistency, read/write profile, integrations, any explicit words such as "distributed", "scalable", "real-time").
3. **List gaps and ambiguities** in the requirements (missing stories, unclear ownership, missing non-functional figures). These become open questions later, so phrase them so anyone can answer them.
4. **Propose three genuinely different architectures** (by default a modular monolith, microservices with synchronous REST, and event-driven, unless the requirements suggest others). For each give: components, pros, cons, and the painful implementation parts. Keep the overview short in chat and put the detail in the notes.
5. **Answer follow-up questions** one at a time. Each answer goes into the notes as a new `Qn` section. Give a diagram when a flow or structure is being discussed (see diagram rule).
6. **Compare** the three in a table (see the table rule) and **recommend exactly one** of them.
7. When the user summarises their understanding, confirm what is right and add only what is genuinely missing (for example redundancy, or the trade-off they must be able to name).

## Phase 2 – ADR

1. Read all inputs (notes, conversation transcripts). The final decision in the discussion is the decision of the ADR. If the discussion changed its mind (e.g. a hybrid was dropped), use the final position and mention the rejected option in the rationale.
2. Write the ADR from `templates/ADR_template.md`. All sections are expected; leave one out only if it truly does not apply.
3. Run the **self-review checklist** (`references/review-checklist.md`) before showing the draft. Fix what it finds, and log those fixes in the notes.
4. Show the user a short summary of what the version contains and anything you corrected compared with the inputs. Then wait for feedback.
5. After each round of feedback, edit the ADR with targeted changes (do not rewrite unrelated sections), rerun the checklist for the parts you touched, and add a change-log entry.

## Quality rules

These were each a correction in an earlier session.

**Pick one of the compared options.** Do not recommend a hybrid of two options that were compared separately. A hybrid usually keeps all the infrastructure of both, so it is more work, not less, and it was not part of the comparison. If a pure option has weak points, handle them inside that option (redundancy, timeouts, idempotency, retry jobs) and list them as mitigations.

**Check every explicit requirement against every option.** If the brief says "distributed", say for each option whether and how it is distributed (by replication / X-axis, or by functional decomposition / Y-axis of the scale cube). A requirement that is met only weakly must be named as such, and the weaker reading belongs in open questions plus an "alternative if relaxed" section.

**Do not overstate guarantees.** An external system (payment provider, email, carrier) can never be inside a local ACID transaction. Use the standard pattern: save a pending state locally, call the external system with an idempotency key, treat the provider's webhook or API as the source of truth, and add a reconciliation job. Never treat a browser redirect as proof of payment.

**Map every story to exactly one owner.**
- Static pages with no data or logic (About Us, legal pages) belong to the frontend, not to a backend service. Say so in one sentence under the service table.
- If a story genuinely spans two services, do not just list it twice. Split it by data ownership (who owns which fields) and say how the UI gets both (e.g. API gateway composition).
- Grouping by "it also sends something" is not a reason to assign a story to a service.

**No contradictions between sections.** The decision, the flows and the mitigations may only rely on data and behaviour the requirements confirm. If something is unknown (stock tracking, multiple merchants), it goes into open questions, and the flow says where it would plug in ("if stock is tracked, the stock check belongs in this step"). Cross-reference both ways.

**Keep numbers consistent with the final design.** Recompute any figure carried over from the discussion (e.g. availability of the critical call chain = product of the critical services' availabilities) with the services that are actually critical in the decided design.

**Always include a structure diagram** of the chosen architecture in the ADR, and a flow diagram for the most critical workflow when it helps. Use plain-text ASCII inside a code block so it renders in any Markdown viewer. Show the client, gateway, each service with its own data store, and external systems. Because boxes alone do not show calls, add a short list of the direct service-to-service calls under the diagram. Drawing the diagram often reveals gaps (who receives a webhook, who calls whom); fix the text when it does and log it.

**Compare in a table with a verdict row.** Section "Considered options" must contain a one-line description per option and a comparison table. Rows: how each option meets the key explicit requirement, effort to build, operations, fit for the user stories, consistency of the critical workflow, behaviour when a component fails, and a final **Verdict** row that states the reasoning in one line per option. Put the chosen column in bold.

**Name the accepted trade-off.** The Consequences section must have an explicit "Accepted trade-off" paragraph: what fails, how it fails (safely or not), and why that price is acceptable.

**Redundancy before resilience tricks.** Mitigations start with redundancy (several instances behind a load balancer) for critical services, then timeouts, circuit breakers, retries only on idempotent calls, batch endpoints against N+1, idempotency keys and unique constraints for money, and correlation IDs for tracing.

**Write for any reader.** An ADR must not mention the teacher, the course, the exercise or "the user". Phrase open questions neutrally ("Is replication enough to meet the 'distributed' requirement?"). Course context may appear in the notes and in chat, not in the ADR.

**Use correct terminology.** For example, a replicated monolith is a "horizontally scaled (modular) monolith", not a "distributed monolith", which is the name of an anti-pattern.

## Style

- Clear, concise prose; tables where the reader compares things; short bullet lists otherwise.
- In chat, report what changed and why in a few sentences, and name the files touched. Do not paste the whole ADR back.
- Prefer targeted edits over full rewrites when revising.

## Files in this skill

- `templates/ADR_template.md` – ADR structure with guidance in each section.
- `templates/notes_template.md` – notes structure for Phase 1 and Phase 2.
- `references/review-checklist.md` – self-review to run before showing any ADR version.
