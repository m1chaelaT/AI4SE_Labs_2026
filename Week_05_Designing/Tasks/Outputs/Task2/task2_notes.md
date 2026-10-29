# Task 2 – ADR session notes

## Inputs
- Task1_notes.md: CDC summary, architectures A/B/C, discussion Q1–Q6, comparison table and recommendation.
- Conversation PDF (29 Oct 2026): the Task 1 discussion; final choice was pure B after the B+C hybrid was dropped as more complex than pure B.

## Version 1 (initial draft)
- Format: Status, Context, Considered options, Decision, Rationale, Consequences, Mitigations, Open questions, Alternative.
- Decision: pure B with five services (Auth/User, Catalog, Order incl. cart, Payment, Shipping/Notification).
- Included the checkout flow (PENDING_PAYMENT → Stripe with idempotency key → webhook → PAID), the accepted trade-off (checkout fails safely), and the mitigations without a broker.
- Kept the CDC gaps as open questions and A as a fallback if replication counts as "distributed".

## Change log
*(updated after each round of feedback: what was asked to change and why)*

### Change 1 – About Us moved out of Shipping/Notification
- **Asked:** Stories 10 and 20 (About Us) were assigned to Shipping/Notification.
- **Why:** About Us is a static page with no business logic or data, so it belongs in the frontend, not in a backend service.
- **Done:** Removed 10 and 20 from the Shipping/Notification row (now 9, 23) and added a sentence below the service table saying About Us is served statically by the frontend.

### Change 2 – "Availability" check contradicted the open question on stock
- **Asked:** Checkout step 2 checked "prices and availability", but the open questions say we don't know if stock is tracked.
- **Why:** The ADR can't rely on stock data the CDC never mentions.
- **Done:** Step 2 now checks prices and that the products still exist, and says the stock check would go there if stock is tracked. The stock open question now points back to step 2.

### Change 3 – Story 9 responsibility between Order and Shipping/Notification
- **Asked:** Story 9 appeared in both services without saying who does what.
- **Why:** Shared ownership of one story is unclear; each piece of data should have one owner.
- **Done:** Added a paragraph: Order owns the order status, Shipping/Notification owns shipment data (carrier, tracking number, delivery status), and the API gateway combines both for the tracking page.

### Change 4 – Diagram of architecture B
- **Asked:** A simple diagram with the client, API gateway, services with their own databases, and Stripe.
- **Done:** Added an ASCII diagram in the Decision section (plain text so it works in any Markdown viewer), plus a short list of the direct service-to-service calls. While drawing it, clarified checkout step 5: Stripe's webhook goes to Payment, which reports the result to Order.

### Change 5 – Comparison table in section 2
- **Asked:** Section 2 was only a list of options; turn it into a small A/B/C comparison table.
- **Why:** The reader should see at a glance why B was chosen.
- **Done:** Kept one-line descriptions of each option and added a table (distribution, build effort, operations, fit for the stories, checkout consistency, failure behaviour, verdict), with the B column in bold.

### Change 6 – Open question without "the teacher"
- **Asked:** Rephrase "Does the teacher accept…" in the open questions.
- **Why:** An ADR should be readable by anyone, not only in the course context.
- **Done:** Now asks whether running several copies of one application (replication) is enough to meet the "distributed" requirement.
