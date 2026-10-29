# ADR self-review checklist

Run this before showing any ADR version. Each item comes from a correction the user had to ask for in an earlier session. Fix what fails, then log the fix in the notes.

## Decision
- [ ] The decision is exactly one of the compared options, not a hybrid.
- [ ] It matches the final position of the discussion, not an earlier draft.
- [ ] Every explicit requirement in the brief (e.g. "distributed") is evaluated for every option, including how it is met.

## Story mapping
- [ ] Every story number appears in the service table exactly once, or is explicitly split.
- [ ] Static pages (About Us, legal, FAQ) are assigned to the frontend, with one sentence saying so.
- [ ] Any story listed under two services has a paragraph stating which data each service owns and how the UI combines them.
- [ ] No story is assigned to a service only because it loosely "sends something".

## Consistency
- [ ] The flows and mitigations rely only on data the requirements confirm. Anything unknown is in open questions, and the flow says where it would plug in.
- [ ] Open questions and the sections they affect point to each other.
- [ ] Figures carried over from the discussion are recomputed for the decided design (e.g. chained availability of the services that are actually critical).
- [ ] No external call is described as part of a local ACID transaction; payment uses pending state + idempotency key + webhook/API as source of truth + reconciliation.

## Presentation
- [ ] Section 2 has a one-line description per option and a comparison table with a Verdict row; the chosen column is in bold.
- [ ] Section 3 has a plain-text structure diagram (client, gateway, services with own data stores, external systems).
- [ ] Under the diagram is a list of direct component-to-component calls, consistent with the flow steps (e.g. who receives the provider's webhook).
- [ ] Consequences has an explicit "Accepted trade-off" paragraph.
- [ ] Mitigations start with redundancy for critical components.

## Audience and wording
- [ ] No mention of the teacher, the course, the exercise or "the user".
- [ ] Open questions are neutral and say what each answer would change.
- [ ] Terms are used correctly (e.g. "horizontally scaled monolith", not "distributed monolith").
