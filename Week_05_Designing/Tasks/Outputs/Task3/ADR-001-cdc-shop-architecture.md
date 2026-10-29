# ADR-001: Microservices with synchronous REST for the CDC shop

- **Status:** Accepted
- **Date:** 2026-10-29
- **Scope:** overall system architecture of the CDC shop (all 25 user stories)

## 1. Context

The CDC shop sells hardware-store materials online. Its brief describes it as a **distributed system** that handles three concerns: the management of products, their payment and their shipment. Two roles use it: **Customers** browse, search and sort products, keep a cart, pay, track their package and contact the shop, and **Merchants** log in to a merchant page and maintain products and prices. About Us is a static page for both roles.

Quality attributes that drive the decision:

- **Distribution** is the only explicit non-functional requirement.
- **Consistency of the checkout (story 7):** a customer must never be charged without an order, an order must never be marked paid without a confirmed charge, and the price paid must be the price shown at checkout.
- **Read-heavy catalog:** eight stories read the catalog (5, 6, 11, 12, 17, 18, 21, 22), only two write to it (15, 16).
- **Security:** authentication for both roles; only merchants may change products and prices; card data stays with an external payment provider.
- **External integrations:** a payment provider, a shipping carrier and e-mail. None of them can take part in a local transaction.

The brief gives no figures for load, availability or response time. Open questions are listed in section 8.

## 2. Decision drivers

1. Meet the "distributed" requirement in its strong reading (functional decomposition), not only by replication.
2. Keep the checkout safe: no lost money and no paid order without a charge, even when a component or the provider fails.
3. Let the read-heavy catalog scale independently of checkout.
4. Keep the system understandable and buildable for a feature set of 25 mostly request/response stories.

## 3. Considered options

- **A – Horizontally scaled modular monolith:** one application with strict internal modules and one database, run as several identical instances behind a load balancer.
- **B – Microservices with synchronous REST:** one service per functional area, each with its own database, behind an API gateway, communicating over REST.
- **C – Event-driven microservices:** the same services as B, communicating mainly through a message broker, with the checkout as a choreographed saga.

| Criterion | A – Modular monolith | **B – Microservices, sync REST** | C – Event-driven |
|---|---|---|---|
| Meets "distributed" | Weakly: replication only (X-axis of the scale cube) | **Yes: functional decomposition (Y-axis), each service also replicated (X-axis)** | Yes: functional decomposition with asynchronous coupling |
| Effort to build | Low | **Medium: seven small services, gateway, explicit checkout consistency** | High: services plus broker, outbox, idempotent consumers, saga compensations |
| Operations | One deployable, one database | **Seven deployables and databases, gateway, tracing** | As B plus a critical message broker |
| Fit for the user stories | Good: stories are mostly CRUD | **Good: request/response matches the stories** | Poor: asynchronous machinery for stories that do not need it |
| Consistency of checkout | Local transaction for order and cart; provider still needs pending state and webhook | **Pending order, idempotency keys, webhook as source of truth, reconciliation** | Eventually consistent saga; UI must show "processing" for every step |
| Behaviour when a component fails | One faulty deployment or database affects every feature | **Failure of a service in the checkout chain stops checkout safely; browsing continues** | Services keep accepting work while others are down; failures surface later and are harder to trace |
| **Verdict** | Simplest, but meets "distributed" only in the weak reading | **Chosen: meets "distributed" clearly at a cost that fits 25 stories** | Solves decoupling problems the stories do not have, at the highest cost |

## 4. Decision

The CDC shop is built as **microservices communicating over synchronous REST** (option B). A single API gateway is the entry point for the web frontend; every service owns its own database and no service reads another service's tables.

A hybrid of B and C (REST plus a broker for selected events) was not chosen: it would keep the full infrastructure of both options and was not part of the comparison. The weak points of B are handled inside B with the mitigations in section 6.

### 4.1 Services and story ownership

| Service | Stories | Owned data |
|---|---|---|
| Identity | 1, 2, 3, 8, 13, 14, 19 | accounts, roles (Customer, Merchant), password hashes, refresh tokens, profiles |
| Catalog | 5, 6, 11, 12, 15, 16, 17, 18, 21, 22 | products, current prices, name index for search |
| Cart | 4, 24, 25 | carts and cart items (product ID, quantity) |
| Order | 7 (order part) | orders, order lines with a price snapshot, order status |
| Payment | 7 (payment part) | payment attempts, idempotency keys, provider references and events |
| Shipping | 9 | shipments, carrier tracking numbers, package status |
| Contact | 23 | contact messages |

About Us (stories 10 and 20) is a static frontend page with no data or logic, so it has no backend service.

Two stories span two services and are split by data ownership:

- **Story 7 (pay for the cart):** Order owns the order and its lines; Payment owns the payment attempt and the relationship with the provider.
- **Story 9 (package information):** Shipping owns the package status and tracking data; the order summary shown next to it comes from Order. The API gateway composes both into one response.

Customer and Merchant variants of the same capability (sort, search, list, details, profile, logout) are served by the same endpoints; only authorisation differs. Product changes (15, 16) require the Merchant role.

### 4.2 Structure

```
                         ┌────────────────────┐
  Web frontend ─────────►│    API gateway     │  JWT validation, routing,
  (incl. About Us)       │  (2+ instances)    │  composition (story 9)
                         └─────────┬──────────┘
        ┌──────────┬───────────┬───┴──────┬───────────┬───────────┬──────────┐
        ▼          ▼           ▼          ▼           ▼           ▼          ▼
   ┌─────────┐┌─────────┐┌─────────┐┌─────────┐┌──────────┐┌──────────┐┌─────────┐
   │Identity ││ Catalog ││  Cart   ││  Order  ││ Payment  ││ Shipping ││ Contact │
   └────┬────┘└────┬────┘└────┬────┘└────┬────┘└────┬─────┘└────┬─────┘└────┬────┘
        ▼          ▼          ▼          ▼          ▼           ▼           ▼
      [DB]       [DB]       [DB]       [DB]       [DB]        [DB]        [DB]
                                                    │           │           │
                                                    ▼           ▼           ▼
                                             Payment provider  Carrier    E-mail
                                             (webhook → gateway → Payment)
```

Direct service-to-service calls (all other traffic goes from the gateway to a single service):

- Cart → Catalog: batch lookup of product names and current prices when a cart is shown or an item is added.
- Order → Cart: read the cart at checkout; empty it after payment is confirmed.
- Order → Catalog: batch lookup of current prices at checkout (price snapshot).
- Order → Payment: start a payment for an order.
- Payment → Order: report that a payment succeeded or failed.
- Order → Shipping: create a shipment for a paid order.

Identity is not called by other services: the gateway validates access tokens with Identity's public key, so Identity is not on the checkout path.

### 4.3 Checkout flow (story 7)

```
 Customer    Gateway     Order        Cart     Catalog    Payment      Provider
    │ Pay ──────►│──────────►│            │         │          │            │
    │            │           │─ get cart ►│         │          │            │
    │            │           │─ batch prices ──────►│          │            │
    │            │           │ save order PENDING_PAYMENT (price snapshot)  │
    │            │           │─ start payment (key = orderId) ►│            │
    │            │           │            │         │          │─ create ──►│
    │◄─────────── redirect URL to hosted payment page ─────────│            │
    │ pays on provider page ───────────────────────────────────────────────►│
    │◄── redirect back: "payment processing" (not proof of payment)         │
    │            │◄──────────── signed webhook ─────────────────────────────│
    │            │──────────────────────────────────────────►│ verify, PAID │
    │            │           │◄── payment succeeded ───────────│            │
    │            │           │ order PAID → create shipment (Shipping), empty cart
```

1. The frontend sends the checkout request with a client-generated idempotency key; Order rejects duplicates through a unique constraint on that key.
2. Order reads the cart and fetches current prices in one batch call. A product that was removed (story 16) fails the checkout with a clear message. If stock is tracked (open question 3), the stock check or reservation belongs in this step.
3. Order saves the order as `PENDING_PAYMENT` with the price snapshot in one local transaction.
4. Order asks Payment to start the payment, using the order ID as idempotency key. Payment saves a `PENDING` attempt and calls the provider with the same key, so repeated calls never create a second charge.
5. The browser redirect back from the provider only shows "payment processing". It is never treated as proof of payment.
6. The provider's signed webhook, which reaches Payment through a public gateway route without JWT authentication, is the source of truth. Payment records the provider event ID (so duplicate webhooks are ignored), marks the attempt `SUCCEEDED` or `FAILED` and reports it to Order.
7. On success Order marks the order `PAID`, then asks Shipping to create the shipment and Cart to empty itself. Both calls are idempotent on the order ID. On failure the order becomes `PAYMENT_FAILED` and the cart is kept.

## 5. Consequences

### Positive

- The system is distributed by function: each concern named in the brief (management, payment, shipment) has its own service and database, and each service can be replicated.
- The catalog, which carries most of the traffic, scales independently of checkout.
- Payment is isolated: only one small service talks to the provider and holds payment state.
- Request/response matches the stories, so each flow can be followed and tested end to end.

### Negative

- The checkout depends on a synchronous chain (gateway, Order, Cart, Catalog, Payment). Its availability is the product of the availabilities in the chain. With an assumed 99.9 % per component and one instance each, that is 0.999⁵ ≈ 99.5 %, noticeably lower than any single component.
- Consistency across services is not automatic; it relies on the pending states, idempotency keys and jobs described in section 6.
- Seven services, seven databases and a gateway must be deployed, monitored and traced, which is considerable operational work for 25 stories.
- Network calls add latency, and a naive cart view would cause N+1 calls to Catalog.

### Accepted trade-off

If Order, Cart, Catalog or Payment is unavailable, checkout fails while browsing, search and profiles continue to work. It fails safely: no charge is made before a pending order exists, a retried request with the same idempotency key cannot charge twice, and a charge whose confirmation is delayed is completed later from the provider's records. This lower checkout availability, together with the operational cost of separate services, is accepted in exchange for a system that is distributed by function and whose payment and catalog parts can be scaled and changed independently. Redundancy (section 6) reduces the availability penalty to an acceptable level.

## 6. Mitigations

1. **Redundancy:** at least two instances of the gateway and of every service on the checkout path (Order, Cart, Catalog, Payment) behind a load balancer; services are stateless. If instances fail independently, two instances at 99.9 % give about 99.9999 % per service, so the chain of five stays above 99.99 % (correlated failures such as a shared database outage are not covered by this figure).
2. **Timeouts and circuit breakers** on every service-to-service call, so a slow service fails fast instead of blocking the chain.
3. **Retries only on idempotent calls:** reads, and writes carrying an idempotency key (start payment, create shipment, empty cart).
4. **Batch endpoint** in Catalog (`POST /products/batch`) used by Cart and Order, avoiding N+1 calls.
5. **Idempotency keys and unique constraints for money:** client key on checkout, order ID towards Payment and the provider, provider event ID on webhooks.
6. **Recovery jobs:** Payment's reconciliation job queries the provider for attempts still `PENDING` after a timeout; Order's retry job completes `PAID` orders that have no shipment or a cart that was not emptied.
7. **Correlation IDs** set by the gateway and passed on every call and log line, so one checkout can be traced across services.
8. **Security:** password hashes with a slow algorithm, short-lived access tokens plus refresh tokens revoked on logout (stories 8, 13), role check for product changes, webhook signature verification.

## 7. Alternative if "distributed" is relaxed

If replication alone is accepted as meeting the "distributed" requirement (open question 1), option A becomes the better choice: the same functional areas as modules of one horizontally scaled application, a checkout whose order and cart changes happen in one local transaction, and a fraction of the operational effort. The module boundaries in section 4.1 would still apply, so splitting into services later stays possible. The payment flow with pending order, webhook and reconciliation would remain unchanged, because the provider is external in either option.

## 8. Open questions

1. Is functional decomposition required, or would replication of one application be enough to meet the "distributed" requirement? (See section 7.)
2. Is there one shop with several merchant accounts, or several independent merchants? If products have different owners, Catalog needs a merchant field and the checkout (section 4.3) would split an order per merchant.
3. Is stock tracked? If so, the stock check or reservation plugs into step 2 of the checkout flow.
4. How are merchant accounts created? Only merchant login (story 14) is described.
5. Who updates the package status shown in story 9: a carrier integration (webhook or polling in Shipping) or the merchant?
6. Which payment provider will be used, and does it offer a hosted payment page with signed webhooks, as assumed in section 4.3?
7. Should contact messages (story 23) be stored for merchants to read, sent by e-mail, or both?
8. Should customers be able to remove a single item or change quantities in the cart? Only adding (24) and emptying (25) are described.
9. What should the cart show when a merchant changes the price (15) or removes a product (16) after it was added? The current design always shows the current price and blocks checkout for removed products.
10. What load, availability and response-time targets apply, and are refunds or cancellations in scope?
