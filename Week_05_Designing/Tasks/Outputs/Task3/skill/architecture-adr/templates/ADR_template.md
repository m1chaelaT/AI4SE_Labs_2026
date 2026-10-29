# ADR-<NNN>: <Decision in one line, e.g. "Use microservices with synchronous REST for X">

- **Status:** Proposed | Accepted | Superseded by ADR-<NNN>
- **Date:** <YYYY-MM-DD>
- **Author:** <name>
- **Related:** <notes file, earlier ADRs, requirements document>

## 1. Context

<!-- What the system does, its roles, and the explicit wording of key requirements (e.g. "distributed"). -->

The forces that shape the decision are:

- **<Explicit requirement>.** <What it demands of the architecture.>
- **<Interaction profile>.** <e.g. most stories are simple request–response.>
- **<Critical workflow>.** <e.g. checkout with an external payment provider; what must never happen.>
- **<Load profile>.** <e.g. read-heavy catalog.>
- **<External integrations>.**
- **<Project scope / team size>.**

<!-- Say which non-functional figures are missing and point to section 7. -->

## 2. Considered options

- **A – <name>:** <one line>
- **B – <name>:** <one line>
- **C – <name>:** <one line>

<!-- Bold the chosen column. Keep the Verdict row: it is the at-a-glance reason. -->

| Criterion | A – <name> | B – <name> | C – <name> |
|---|---|---|---|
| Meets "<key requirement>" | | | |
| Effort to build | | | |
| Operations | | | |
| Fit for the user stories | | | |
| Consistency of <critical workflow> | | | |
| When a component fails | | | |
| Verdict | | | |

## 3. Decision

We will build <system> as **<chosen option>**, <one sentence on shape>.

<!-- Every story appears exactly once across the table, or is explicitly split below. -->

| Service / module | Responsibility | User stories |
|---|---|---|
| | | |

<!-- Static pages: "The <page> (stories n, m) is static content served by the frontend." -->
<!-- Split stories: who owns which data, and how the UI combines them. -->
<!-- Deliberate boundary decisions, e.g. "cart and orders in one service because their data changes together." -->

**Structure:**

```
<ASCII diagram: client -> gateway -> services, each with its own data store -> external systems>
```

Besides the gateway routes, the components call each other directly only in these places:

- <A → B: purpose (flow step n)>

**<Critical workflow> flow:**

1. <step>
2. <step; if something is unknown in the requirements, say where it would plug in and point to section 7>

## 4. Rationale

- **<Option> satisfies <key requirement>.** <how, compared with the others>
- **<Fit for the stories.>**
- **<Why not the more complex option.>**
- **<Why rejected alternatives such as a hybrid were dropped, if discussed.>**

## 5. Consequences

### Positive

-

### Negative

<!-- Recompute numbers (e.g. chained availability) with the services actually critical in this design. -->

-

### Accepted trade-off

<!-- What fails, how it fails (safely?), and why this price is acceptable. -->

## 6. Mitigations

<!-- Start with redundancy, then resilience patterns, idempotency, tracing. -->

| Risk | Mitigation |
|---|---|
| | |

## 7. Open questions

<!-- Neutral wording, no mention of teacher/course. Each should say what it would change. -->

These gaps in the requirements may affect the design and should be confirmed:

-

## 8. Alternative if <a requirement> is relaxed

<!-- The simplest correct solution under the weaker reading, and what stays the same. -->
