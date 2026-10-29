# Comparison report: ADR without and with the `architecture-adr` skill

**System:** CDC shop | **Author:** Michaela Tóthová | **Date:** 2026-10-29

## Introduction

This report compares two ways of reaching the same goal for the CDC shop: proposing three architectures, choosing one and documenting the decision in an Architecture Decision Record. In the first run, I did this manually in two sessions, first discussing the architectures (Task 1) and then iterating on the ADR (Task 2). In the second run, I used the `architecture-adr` skill, which the assistant created from the recordings and notes of the first run, in a single new session with only `CDC.txt` and a one-line prompt. Both runs ended with the same decision: microservices with synchronous REST.

## Effort

The manual run took two sessions and about fourteen of my messages. In Task 1, I had to guide the discussion step by step and twice correct the assistant's claims: it first presented the checkout in the monolith as one ACID transaction, although the external payment provider cannot be part of it, and later recommended a hybrid of two architectures instead of one of the compared options. In Task 2, the first version of the ADR needed six corrections over three rounds of feedback before I was satisfied.

With the skill, the whole task took one session and two messages: the initial request and the instruction to go with option B and write the ADR. **The ADR created with the skill needed no correction at all.** When I reviewed it, it was complete and correct in its first version.

## Were the earlier mistakes avoided?

All the problems I had to point out in the manual run were handled correctly from the start. The About Us page was treated as a static frontend page rather than a backend service, and the checkout flow did not rely on stock tracking, which the requirements never mention. Stories that span two services, such as order tracking and payment, were split clearly by data ownership. The ADR included a comparison table of the three options and a structure diagram without being asked, and it was written neutrally, without references to the course or the teacher.

The skill also made the assistant review its own work. While drawing the diagrams, it found four gaps in its earlier notes by itself, for example a missing call from the cart to the catalog and an unclear route for the payment webhook, and it fixed and logged them before showing me the result. In the manual run, I had to discover this kind of inconsistency myself.

## Quality of the final ADRs

Both ADRs have a similar structure, but the one created with the skill is more thorough. It assigns each of the 25 user stories to exactly one service, adds a separate checkout sequence diagram, describes the failure path and duplicate webhooks in the checkout flow, and recalculates availability with and without redundancy. Its open questions are also more concrete, since each one points to the part of the design it would affect. The manual ADR is shorter and easier to read quickly, and its design with five services is somewhat simpler to operate than the seven services in the skill version.

## Remaining weaknesses

The skill version is about 40 % longer, so a short summary at the top would help readers who only need the decision. The skill saved to my account was missing its template and checklist files, so the assistant worked only from the main instructions. The result was still correct, but the complete skill folder should be used. Finally, because the skill does so much of the work, the discussion in the second run was very short. The skill speeds up producing the ADR, but understanding the trade-offs still depends on the user asking questions.

## Conclusion

The skill clearly achieved its purpose. The same result took one session instead of two and two messages instead of about fourteen, and the ADR needed no corrections instead of six. The lessons learned from the manual run were applied automatically, and the final document is more detailed and consistent than the one I created through iterative feedback.
