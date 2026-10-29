# Notes templates

Use the part that matches the phase. Update the file after every step and every answer.

---

## Phase 1 – Architecture discussion notes

```markdown
# <System> – Architecture Notes

## 1. System summary
<What the system does, roles and what each role can do.>

### Functional areas (derived from user stories)
| Area | Stories |
|---|---|
<!-- Every story exactly once. Static pages get their own row. -->

### Key requirements / quality attributes
- **<attribute>**: <why it matters here>

### Gaps and ambiguities in the requirements
- <question> <what it would change>

---

## 2. Architecture proposals (overview)
### A) <name>
- **Components**:
- **Pros**:
- **Cons**:
- **Painful parts**:
### B) <name>
...
### C) <name>
...

---

## 3. Discussion log
*(updated as we go)*

### Q1 – <topic of the question>
<Answer in note form. Include plain-text diagrams. If an earlier note was wrong, say so here.>
**Takeaway.** <one or two sentences>

---

## 4. Comparison of A, B and C
| Criterion | A | B | C |
|---|---|---|---|

### Recommendation
**Pick: <exactly one of A, B, C>.**
<Why, how its weak points are handled within the option, the accepted trade-off,
and the alternative if a requirement is read more loosely.>
<If an earlier recommendation was dropped, note it and why.>
```

---

## Phase 2 – ADR session notes

```markdown
# <Task> – ADR session notes

## Inputs
- <file>: <what it contained>

## Version 1 (initial draft)
- Format: <sections used>
- Decision: <one line>
- <key content>
- Corrections compared with the inputs: <e.g. availability recomputed for 3 critical services>

## Change log
*(updated after each round of feedback: what was asked to change and why)*

### Change 1 – <short title>
- **Asked:** <what the user pointed out or requested>
- **Why:** <the reason behind it>
- **Done:** <what was changed, and where>
```
