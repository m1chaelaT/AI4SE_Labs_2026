# ADR-001: Use microservices with synchronous REST for CDC Shop

- **Status:** Proposed
- **Date:** 2026-10-29
- **Author:** Michaela Tóthová
- **Related:** Task1_notes.md (architecture comparison, discussion Q1–Q6)

## 1. Context

CDC Shop is an online hardware store with two roles. **Customers** register, log in, browse, search and sort products, manage a cart, pay, track orders and contact the shop. **Merchants** log in, manage the catalog (insert and remove products) and change prices. The CDC explicitly describes the system as **distributed**.

The forces that shape the decision are:

- **Distribution requirement.** The CDC asks for a distributed system, so the architecture must be distributed in design, not only in deployment.
- **Mostly simple interactions.** The majority of user stories (browsing, search, profile, cart, merchant CRUD) are request–response operations with no complex workflow.
- **Safe checkout.** Checkout involves an external payment provider (Stripe), so it can never be a single ACID transaction. The system must never charge a customer without recording the order, and never confirm an order that was not paid.
- **Read-heavy catalog.** Browsing and searching happen far more often than merchant writes.
- **External integrations.** Payment gateway, shipping carrier and email.
- **Project scope.** A small team in a university setting, so build and operational complexity must stay manageable.

The CDC gives no non-functional figures (number of users, availability, response times) and leaves several domain questions open (see section 7).

## 2. Considered options

- **A – Modular monolith:** one deployable backend with feature modules and one relational database.
- **B – Microservices with synchronous REST:** independently deployable services, each with its own database, behind an API gateway.
- **C – Event-driven:** services communicating mainly through events over a message broker, with checkout as a saga.

| Criterion | A – Modular monolith | B – Microservices (REST) | C – Event-driven |
|---|---|---|---|
| Meets "distributed" | Weakly, only by running copies | **Yes**, by splitting into services | Yes |
| Effort to build | Low | **Medium** | High |
| Operations | One app, one database | **Several services, gateway, logging** | Like B, plus a broker as critical infrastructure |
| Fit for the user stories (mostly simple requests) | Good | **Good**, request–response | Weaker, most stories don't need events |
| Checkout consistency | Local transactions; only Stripe needs care | **Coordinated by Order through API calls** | Eventual; outbox, idempotent consumers, saga compensations |
| When a service fails | Whole app is affected | **Failure stays in one service, but checkout needs Order, Payment and Catalog up** | Services can be briefly down; risk of duplicate, lost or reordered events |
| Verdict | Simplest, but fails the main driver | **Chosen**: meets the driver at moderate cost | Meets the driver, but too complex for this shop |

## 3. Decision

We will build CDC Shop as **a small number of microservices communicating over synchronous REST (option B)**, behind an API gateway, with a separate database per service:

| Service | Responsibility | User stories |
|---|---|---|
| **Auth/User** | Registration, login/logout, profiles, Customer/Merchant roles | 1, 2, 3, 8, 13, 14, 19 |
| **Catalog** | Product list, detail, search, sort; merchant CRUD and price changes | 5, 6, 11, 12, 15–18, 21, 22 |
| **Order** | Cart and orders together, checkout coordination, order status | 4, 9, 24, 25 |
| **Payment** | Wraps Stripe; creates and confirms payments | 7 |
| **Shipping/Notification** | Shipment and package info, emails, contact form | 9, 23 |

The About Us page (stories 10 and 20) is static content served by the frontend, so it needs no backend service.

Story 9 (order tracking) is split between two services by what each one owns. Order owns the **order status** (`PENDING_PAYMENT`, `PAID`, `FAILED`). Shipping/Notification owns the **shipment data** (carrier, tracking number, delivery status), which it creates once Order hands over a paid order. The tracking page gets both through the API gateway, which combines the two responses, so neither service has to keep a copy of the other's data.

Cart and orders live in one service on purpose, because their data changes together during checkout. Services never read each other's databases; they exchange data only through the owning service's API.

**Structure:**

```
+---------------------------------------------------------------------+
|      Web client: Customer + Merchant UI, static About Us page       |
+---------------------------------+-----------------------------------+
                                  | HTTPS / REST
+---------------------------------v-----------------------------------+
|        API gateway: routing, JWT check, response composition        |
+---------------------------------------------------------------------+
      |             |             |             |              |
+-----v-----+ +-----v-----+ +-----v-----+ +-----v-----+ +------v------+
| Auth/User | |  Catalog  | |   Order   | |  Payment  | |  Shipping/  |
|           | |           | |  (+ cart) | |           | | Notification|
|-----------| |-----------| |-----------| |-----------| |-------------|
|  Auth DB  | | Catalog DB| |  Order DB | | Payment DB| | Shipping DB |
+-----------+ +-----------+ +-----------+ +-----+-----+ +------+------+
                                                |              |
                                           +----v----+  +------v------+
                                           | Stripe  |  |Email/carrier|
                                           +---------+  +-------------+
```

Besides the gateway routes, the services call each other directly only in these places (all REST):

- Order → Catalog: batch price check at checkout (step 2 below)
- Order → Payment: create the payment (step 4)
- Stripe → Payment (webhook), then Payment → Order: payment result (step 5)
- Order → Shipping/Notification: hand over the paid order (step 6)

**Checkout flow:**

1. The client calls `POST /orders` on the Order service.
2. Order re-validates the current prices with Catalog in one batch call and checks that the products still exist, since a merchant may have removed them. If a price changed, the customer sees it before paying. Stock is not checked, because the CDC does not say whether it is tracked (see section 7); if it is, the stock check belongs in this step.
3. Order saves the order as `PENDING_PAYMENT`, with a snapshot of the agreed prices.
4. Order calls Payment, which creates a Stripe PaymentIntent with **idempotency key = orderId**.
5. The Stripe webhook is the source of truth. Stripe sends it to Payment, which reports the result to Order, and the order becomes `PAID` or `FAILED`. The browser redirect never counts as proof of payment.
6. Only after `PAID` does Order clear the cart and call Shipping/Notification.

## 4. Rationale

- **B clearly satisfies the distribution requirement.** A is distributed only weakly, through replication of a single deployable unit (scale cube X-axis). B is distributed by functional decomposition (Y-axis).
- **REST matches the user stories.** Most stories are simple requests, which fit request–response naturally.
- **One communication style.** Using only REST keeps the system easier to build, test and explain than C.
- **C's hardest problems are not needed.** A shop of this size does not justify a message broker, transactional outboxes, handling of duplicate or reordered events, and saga compensations.
- **A hybrid of B and C was rejected.** It would need both REST and a broker with outboxes, so it would be more work than pure B, not less.

## 5. Consequences

### Positive

- Services can be deployed and scaled independently, for example scaling only Catalog for heavy browsing.
- A failure in a non-critical service (Shipping/Notification) does not affect browsing or checkout.
- Clear ownership of data: Catalog owns the current price, the cart keeps a display snapshot, and the order keeps the price the customer agreed to pay.

### Negative

- **Checkout depends on several services at once.** Order, Payment and Catalog must all be reachable. Availabilities multiply (three services at 99.9 % give about 99.7 %).
- **Latency adds up** with each network hop.
- **Higher operational cost** than a monolith: several deployments, an API gateway, centralised logging and tracing.
- **No shared transaction**, so consistency across services has to be designed explicitly.
- **Integration testing is harder** than testing a single process.

### Accepted trade-off

If Order, Payment or Catalog is unreachable at checkout, checkout fails. It fails **safely**: the customer is not charged and keeps the cart. This is the price of avoiding the complexity of C.

## 6. Mitigations

| Risk | Mitigation |
|---|---|
| Catalog (or another critical service) down | Run at least two instances behind a load balancer; call Catalog before Payment so failure happens before any charge |
| Slow service causing cascading failure | Timeouts on every remote call (1–2 s), circuit breakers (e.g. Resilience4j), few retries with backoff, only on idempotent calls |
| Double charge | Stripe idempotency key = orderId; unique constraint on `orderId` in the `payments` table; idempotent webhook handler |
| Server crash after Stripe charges | Order is already saved as `PENDING_PAYMENT`; Stripe retries the webhook; a reconciliation job checks stale pending orders against the Stripe API |
| Shipping/Notification call fails after payment | Order keeps a status flag (e.g. `shippingRequested = false`) and a small retry job tries again later; checkout is already complete |
| N+1 calls to Catalog | Batch endpoint `GET /products?ids=…` |
| Hard to follow one order | orderId/traceId passed in an HTTP header; centralised logs |

## 7. Open questions

These gaps in the CDC may affect the design and should be confirmed:

- Is there one merchant or many (marketplace)? This affects the data model and authorisation.
- How do merchants get accounts? There is no merchant registration story.
- Is stock tracked? There are no inventory stories. If yes, checkout step 2 gains a stock check.
- Who updates the shipment status: the merchant or a carrier API?
- Should a customer be able to remove a single item from the cart?
- What are the expected load, availability and response-time targets?
- Is running several copies of one application (replication) enough to meet the "distributed" requirement? If yes, see section 8.

## 8. Alternative if the distribution requirement is relaxed

If replication counts as "distributed", a **horizontally scaled modular monolith (A)** is the simplest correct solution: identical stateless instances behind a load balancer, sessions in JWT or Redis, a shared database, and background jobs guarded by a distributed lock. The checkout pattern with Stripe (sections 3 and 6) stays the same.
