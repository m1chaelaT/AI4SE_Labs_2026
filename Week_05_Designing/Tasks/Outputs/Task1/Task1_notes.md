# CDC Shop – Architecture Notes

## 1. System summary

CDC Shop is an online hardware store. It manages products, payment and shipment, and it is described as a **distributed system**. There are two user roles:

- **Customer**: registers, logs in and out, views the profile, browses and searches products (sort by price, search by name, product detail), manages a cart (add items, clear cart), pays, tracks orders and package info, contacts the shop, and views About Us.
- **Merchant**: logs in and out (separate Merchant page), views the profile, browses and searches products, inserts and removes products, changes prices, and views About Us.

### Functional areas (derived from user stories)

| Area | Stories |
|---|---|
| Identity & accounts (register, login, logout, profile, roles) | 1, 2, 3, 8, 13, 14, 19 |
| Catalog (list, detail, search, sort) | 5, 6, 11, 12, 17, 18, 21, 22 |
| Catalog management (CRUD, price changes) | 15, 16 |
| Cart | 4, 24, 25 |
| Payment / checkout | 7 |
| Orders & shipment tracking | 9 |
| Static / contact (About Us, contact form) | 10, 20, 23 |

### Key requirements / quality attributes

- **Security**: authentication, role-based authorisation (Customer vs Merchant), safe handling of payment (an external payment provider, PCI concerns).
- **Consistency at checkout**: cart → payment → order must not lose money or create orders that were never paid for. Price changes made while a customer is checking out also need handling.
- **Read-heavy catalog**: browsing and search happen far more often than writes, so caching and search indexing help.
- **Integration with external systems**: payment gateway, shipping carrier (tracking info), email for contact and notifications.
- **Distribution**: the brief explicitly says "distributed", which matters when choosing an architecture.

### Gaps and ambiguities in the CDC (worth raising)

- Is there one merchant or many (a marketplace)? This changes the data model and authorisation.
- How do merchants get accounts? No registration story exists for them.
- There are no stock or inventory stories. Can a customer buy an item that is out of stock?
- Shipment is only implied (story 9). Who updates the shipment status: the merchant or a carrier API?
- There is no story for removing a single item from the cart, only for clearing the whole cart (story 25).
- No non-functional figures are given (expected users, availability, response times).

---

## 2. Architecture proposals (overview)

### A) Layered monolith (3-tier client–server)
One backend application with presentation, business and data layers, one relational DB, and a web front end. "Distributed" here means only client and server, plus external services.

- **Components**: web client (SPA or server-rendered), monolithic backend with modules (Auth, Catalog, Cart, Orders, Payment adapter, Shipping adapter, Contact), a single relational DB, and external payment, shipping and email services.
- **Pros**: simple to build, test and deploy. ACID transactions cover all *internal* data (cart, order, stock); the external payment still needs a separate pattern (see discussion log, Q1). Low operational cost. Well suited to a small team or a university project.
- **Cons**: the whole system scales as one unit. Tight coupling grows over time. One bug or deploy affects everything. It is arguably a weak fit for the "distributed" label.
- **Painful parts**: keeping module boundaries clean so the code doesn't become a "big ball of mud". Making external payment calls inside a DB transaction (timeouts, partial failure). Later migration if the system grows.

### B) Microservices (synchronous REST + API gateway)
The system is split by business capability into independently deployable services, each with its own DB, behind an API gateway.

- **Components**: front end(s) for Customer and Merchant, an API gateway (routing, auth token check), Auth/User service, Catalog service, Cart service, Order service, Payment service (wraps the provider), Shipping service, Notification/Contact service, plus a service registry or discovery and centralised config and logging.
- **Pros**: independent scaling (for example, scale the Catalog for heavy browsing). Independent deployment. Failure isolation. Teams can own services. Clearly "distributed".
- **Cons**: much higher operational complexity (deployment, monitoring, tracing). Network latency. Synchronous call chains are fragile, since one slow service blocks others.
- **Painful parts**: **distributed checkout** (Cart → Order → Payment) without a shared transaction. Data duplication (the price in the cart vs the catalog). Service-to-service authentication. Integration testing. Defining the right service boundaries.

### C) Event-driven architecture (services + message broker)
The services are like those in B, but they communicate mainly through asynchronous events over a broker (e.g. Kafka or RabbitMQ). Checkout is a **saga**.

- **Components**: front ends, API gateway, services (Auth, Catalog, Cart, Order, Payment, Shipping, Notification), a **message broker** with topics such as `OrderPlaced`, `PaymentSucceeded`/`PaymentFailed`, `OrderShipped` and `PriceChanged`, a read-optimised catalog or search view (CQRS-style), and an optional saga orchestrator.
- **Pros**: loose coupling. Services can be down temporarily without blocking others. Workflows such as order → payment → shipment → notification map naturally to events. Easy to add new consumers (analytics, emails).
- **Cons**: **eventual consistency**, so the UI must handle "pending" states. Harder to reason about and debug. The broker is critical infrastructure.
- **Painful parts**: saga design and **compensating actions** (payment fails → cancel the order, release stock). Idempotency and duplicate events. Event ordering. Schema versioning of events. Tracing a single order across many services.

---

## 3. Discussion log
*(updated as we go)*

### Q1 – Architecture A: what is a "modular monolith", and how does checkout work with Stripe?

**Structure of the monolith.** It is one project, built and deployed as a single unit. Folders per feature (cart, orders, products…) are the right start, but folders alone do not make a module. The code should be *packaged by feature* (not by layer), and each module needs three rules:
- **A public API**: other modules call only its service interface (e.g. `CatalogService.getProduct(id)`), never its internal classes.
- **Data ownership**: a module owns its tables. Other modules never query those tables directly; the Order module asks the Catalog module for a price instead of joining on `products`.
- **No cycles**: dependencies go one way, e.g. orders → catalog, never back.

These rules can be enforced with separate build modules (Maven/Gradle multi-module) or with architecture tests (ArchUnit, Spring Modulith). Without enforcement the monolith slowly turns into a "big ball of mud". The payoff is that a well-kept module can later be extracted into a microservice (path A → B).

```
cdc-shop/
  auth/       api/  internal/  (controller, service, repository, entities)
  catalog/    api/  internal/
  cart/       api/  internal/
  orders/     api/  internal/
  payment/    api/  internal/   ← Stripe adapter lives here
  shipping/   api/  internal/
  contact/    ...
  shared/     (common types, config, security)
```

**Checkout with an external payment provider.** The original note claiming that "ACID makes checkout easy" was overstated. A DB transaction cannot include Stripe, because a remote call cannot be rolled back. This is the dual-write problem, and it exists even in a monolith. The standard pattern:

1. **Local transaction**: create the order with status `PENDING_PAYMENT`, snapshot prices from the cart, and reserve stock. Commit.
2. **Call Stripe** outside any DB transaction. Create a PaymentIntent with **idempotency key = order id** and put the order id in its metadata. A retry then never charges twice.
3. **Stripe webhook** (`payment_intent.succeeded` / `payment_failed`) is the source of truth. A second local transaction marks the order `PAID` (or `FAILED` and releases the stock). The handler must be **idempotent**, because Stripe can deliver the same event more than once.

**What if Stripe charges the customer and the server crashes?**
- The order already exists as `PENDING_PAYMENT`, because it was committed before the charge, so nothing is lost.
- Stripe **retries the webhook** for up to several days until the server acknowledges it, so the order becomes `PAID` once the server is back.
- As a safety net, a **reconciliation job** periodically checks old `PENDING_PAYMENT` orders against the Stripe API and fixes their status. Orders abandoned past a timeout get cancelled and their stock released.
- Never trust the browser's redirect ("payment success" page) as proof of payment; only the webhook or an API check counts.

**Takeaway.** Even the monolith has a small distributed workflow at checkout: a state machine of PENDING → PAID/FAILED, made safe by idempotency keys, webhooks and reconciliation. B and C have the same problem, just between more parties.

### Q2 – Is architecture A actually "distributed"? Can we just run more copies?

**Definition.** A distributed system is a set of components on networked machines that coordinate by passing messages and appear to the user as one system.

**Is A distributed?** Technically yes, but weakly. Browser, application server, DB server and the external services (Stripe, carrier, email) run on different machines and talk over the network. All the *business logic* sits in one deployable unit, though, so it is distributed in deployment but not in design. Whether this satisfies the CDC depends on how the teacher reads "distributed", so it is worth asking.

**Running more copies = horizontal scaling (replication).** Several identical instances run behind a **load balancer** (e.g. Nginx). This makes A genuinely distributed at runtime and gives availability: if one instance dies, the others keep serving. It only works if the application is **stateless**, which brings new problems:

- **Sessions / login**: use JWT tokens or a shared session store (Redis), not in-memory sessions. Otherwise users get logged out when the load balancer sends them to another instance.
- **Cart**: store it in the DB or Redis, not in server memory.
- **Background jobs** (the reconciliation job from Q1, abandoned-order cleanup) must run **once**, not once per instance. This needs a distributed lock (DB row lock, ShedLock, Redis) or a dedicated worker instance.
- **Webhooks** can hit any instance, so the idempotent handler from Q1 matters even more (two instances may process the same retry concurrently).
- **Local caches** (e.g. a cached catalog) go stale on the other instances after a merchant changes a price. Use a shared cache (Redis), short TTLs or invalidation messages.
- **Uploaded files** (product images) go to shared/object storage (S3, MinIO), not the local disk.
- **The DB is still a single shared component**, so it is the bottleneck and single point of failure. Mitigations: read replicas for the read-heavy catalog, failover/backup. Replicas bring replication lag (a merchant changes a price and briefly sees the old one).

**Useful framing: the scale cube (AKF).**
- **X-axis = cloning**: identical copies behind a load balancer. This is scaled-out A.
- **Y-axis = functional decomposition**: split by business capability. This is B and C.
- **Z-axis = data partitioning (sharding)**: e.g. split customers or products across DB instances.

A uses X (and optionally Z), while B/C add Y. "Distributed" can mean either, so the honest answer is that **A becomes distributed through replication, B/C through decomposition**.

**Terminology warning (Q2).** Don't call scaled-out A a "distributed monolith". That term names an *anti-pattern*: microservices so tightly coupled that they must be deployed together, which brings the costs of B without its benefits. The correct terms are a *horizontally scaled (modular) monolith* or a *replicated monolith*.

### Q3 – Architecture B: how does a service get data it doesn't own (Cart needs prices, Order needs the cart)?

**Rule.** "Database per service" means that no service reads another service's tables. Data is shared only through the owning service's **API** (or, in C, through its **events**). The owner stays the single source of truth for its data.

**Ways to get the data:**
1. **Synchronous API call**: Cart calls `GET catalog/products/{id}` when a product is added. This is the default in B.
2. **Pass data along in the request**: the caller sends what the callee needs, e.g. Order receives the cart contents in the checkout call.
3. **Local copy kept up to date by events**: Cart keeps a small read-only table of `productId → price, name`, updated from `PriceChanged` events. This is fast and survives Catalog being down, but the copy can be stale. It is the bridge towards architecture C.
4. **API composition for reads**: the gateway or a BFF (backend-for-frontend) calls several services and merges the results for one screen (e.g. the cart page shows items plus product names and images).

**Key idea: snapshots, and different owners of "the price".**
- **Catalog** owns the *current* price.
- **Cart** stores a *snapshot* of the price when an item is added (for display only).
- **Order** stores *its own copy* of the lines and the price the customer actually agreed to pay. An order placed last month must not change when the merchant edits the price today.

This duplication is **intentional**, not a design smell: each copy has a different meaning.

**Checkout flow in B (synchronous):**
1. Client → `POST /orders` on the **Order service**.
2. Order → **Cart**: get the cart items.
3. Order → **Catalog**: batch call `GET /products?ids=…` to **re-validate** the current prices and availability. If a price changed since it was added to the cart, show it to the customer before charging.
4. Order saves the order as `PENDING_PAYMENT` with the snapshot lines.
5. Order → **Payment** service (Stripe, same pattern as Q1).
6. On payment success → Order marks it `PAID` and asks **Cart** to clear (only after payment, so a failed payment doesn't lose the cart).

**Painful parts of this approach:**
- **Availability multiplies**: if checkout needs Order, Cart, Catalog and Payment all up, each at 99.9 %, the chain is ≈ 99.6 %. The more services in a chain, the worse it gets.
- **Latency adds up** with each hop, so batch endpoints are needed instead of one call per product (the N+1 problem).
- **Needed defences**: timeouts, retries (only on idempotent calls), **circuit breakers** (stop calling a failing service), fallbacks (e.g. show cached prices on the cart page, but *never* charge from a stale price).
- **Partial failure in step 6**: the order is paid but the cart-clear call fails. This is harmless if the call is retried; the important state (the order) is already correct.
- **Where synchronous coupling can't be tolerated**, event-based replication (option 3) is used, which leads to architecture C.

### Q4 – Architecture B: what if Catalog (or another service) is down during checkout?

**Short answer.** In a purely synchronous B, yes, checkout fails. The important point is *where* and *how* it fails. In the Q3 flow Catalog is called **before** payment, so it fails safely: no order is confirmed and no money is taken. The customer keeps the cart and can try again. Failing safely is acceptable; charging from unverified data is not.

**Slow is worse than down.** A crashed service answers immediately with a connection error. A slow service ties up Order's threads while they wait, and that can bring Order down too (a **cascading failure**). Defences:
- **Timeouts** on every remote call (e.g. 1–2 s), never wait forever.
- **Circuit breaker**: after repeated failures Order stops calling Catalog for a while and fails immediately with a clear message ("Checkout temporarily unavailable, your cart is saved"). This protects both services (Resilience4j in Java, Polly in .NET).
- **Retries** with backoff, but only a few, and only for idempotent calls.

**Ways to keep checkout working when Catalog is down:**
1. **Make "down" rarer (redundancy)**: run several Catalog instances behind a load balancer, with a replicated DB. This is the first defence, but it doesn't remove the problem.
2. **Local replica in Order**: Order keeps its own read-only copy of prices and availability, fed by `PriceChanged`/`ProductRemoved` events. Checkout no longer needs Catalog at runtime. The trade-off is that the copy may be a few seconds stale. This is a step towards C.
3. **Honour the cart snapshot (business policy)**: accept the price stored in the cart if the snapshot is recent (e.g. < 30 min). This is a **business decision**, not a technical one: the shop must accept the risk of occasionally selling at an old price.
4. **Accept the order asynchronously**: save the order as `PENDING_VALIDATION`, tell the customer "order received", and validate and charge once Catalog is back. This needs good UX for the pending state and clearly leads into C.

**Which services are critical for checkout?**
- **Order, Payment**: essential, no checkout without them.
- **Catalog**: needed for price validation, but replaceable by a replica or snapshot policy (options 2–3).
- **Cart**: its data can be sent by the client in the request (Q3, option 2).
- **Shipping, Notification**: **not needed** for checkout. They can run later (after `PAID`), so their outage must not block payment.

**Takeaway.** Synchronous microservices turn every runtime dependency into a possible point of failure. The design question is which dependencies to keep synchronous (Payment) and which to make asynchronous or replicated (Catalog, Shipping, Notification). Answering that question consistently is basically architecture C.

### Q5 – Architecture C: the hardest parts to code (duplicates, lost events, tracing one order)

**Why duplicates happen.** Brokers (Kafka, RabbitMQ) normally guarantee **at-least-once** delivery, not exactly-once. Typical case: Payment processes `OrderPlaced`, charges the card, then crashes *before* acknowledging the message. The broker redelivers it. So **yes, a naive consumer charges twice.** Duplicates are normal behaviour, not a rare bug, and every consumer must handle them.

**Fix: the idempotent consumer.** Processing the same event twice must have the same effect as processing it once.
- Every event carries a unique **eventId** (and the **orderId**).
- The consumer keeps a `processed_events` table with a unique key on `eventId`. It records the event **in the same local DB transaction** as the business change. A second delivery hits the unique key and is skipped.
- **Natural idempotency** is even better: the `payments` table has a unique constraint on `orderId`, so one order can never have two payments, whatever the events say.
- **Last line of defence at Stripe**: idempotency key = orderId (as in Q1). Even if our code fails, Stripe won't create a second charge for the same key.
- Layering all three is normal for money.

**The opposite problem: lost events (dual write on the producer).** Order must (1) save the order in its DB and (2) publish `OrderPlaced`. If it crashes between the two, the order exists but nobody ever hears about it. If it publishes first and the DB write fails, Payment charges for an order that doesn't exist. This is arguably **the hardest part of C**.
- **Fix: transactional outbox.** In *one* local transaction, Order writes the order **and** a row into an `outbox` table. A separate relay process (polling, or CDC with Debezium) reads the outbox and publishes to the broker, then marks the row as sent.
- The relay may publish a row twice after a crash, so outbox + idempotent consumers = effectively exactly-once.
- **Outbox on the producer side + idempotency on the consumer side** is the standard pair to know for an exam.

**Other hard parts:**
- **Ordering**: `PriceChanged(10 €)` and `PriceChanged(12 €)` can arrive in the wrong order. Kafka keeps order only **within a partition**, so use the productId/orderId as the partition key. Alternatively store a version number and ignore older events.
- **Poison messages**: an event that always crashes the consumer blocks the queue. After N retries it goes to a **dead-letter queue (DLQ)** for manual inspection.
- **Event schema evolution**: old and new versions of a service run side by side during deployment. Only add fields (never rename or remove), and version the events or use a schema registry (Avro/Protobuf).
- **Compensations**: there is no rollback, only new events that undo effects (`PaymentFailed` → `OrderCancelled` → `StockReleased`). Some things can't be undone (an email already sent), so order the steps carefully.
- **Testing**: correctness depends on timing, so test with duplicated, delayed and reordered events, not just the happy path.

**Tracing one order through five services:**
- **Correlation ID**: every event and log line carries the **orderId** (and a **traceId**), passed along in event headers. Each service copies it into the events it emits.
- **Centralised logging** (ELK stack, Grafana Loki): all services send logs to one place, then search `orderId = 1234` to see the whole story across services.
- **Distributed tracing** (OpenTelemetry → Jaeger/Zipkin): shows the order as one timeline of spans (Order → broker → Payment → Shipping…), including where it waited or failed.
- **Order timeline / status view**: a read model built from all order-related events (`PLACED → PAID → SHIPPED`), useful both for debugging and for the customer's "check my order" page (story 9).

**Choreography vs orchestration (affects tracing a lot):**
- **Choreography**: services react to each other's events; there is no central coordinator. Very loosely coupled, but the workflow exists only implicitly across services, so it is hard to see where an order is stuck.
- **Orchestration**: a **saga orchestrator** (e.g. inside Order, or a tool like Temporal or Camunda) sends commands and stores the saga's state explicitly (`WAITING_FOR_PAYMENT`). There is one place to look and compensations are easier to manage, at the cost of a central component.
- For checkout (money, compensations), **orchestration is usually the better choice**. Choreography suits simple fan-out reactions (e.g. `OrderShipped` → send an email).

**Takeaway.** C moves the difficulty from "services being down" (B) to "messages being duplicated, lost, delayed or reordered". The core toolkit: **outbox, idempotent consumers, correlation IDs + tracing, DLQ, orchestrated saga with compensations**.

### Q6 – Architecture C: checkout flow as a diagram (outbox + duplicate checks)

```
[Order service] --(one local tx: order row + outbox row)--> [Outbox relay]
                                                                 | OrderPlaced
                                                                 v
=========================== Message broker ===========================
   | OrderPlaced          ^ PaymentSucceeded          | PaymentSucceeded
   v                      |                           v
[Payment service] --------+                 [Shipping]   [Notification]
 (dup check by eventId)                      (dup check)  (dup check)
   |
   v
[Stripe]  (idempotency key = orderId)

Order service also consumes PaymentSucceeded → marks the order PAID.
```

**Reading the diagram:**
1. Order saves the order **and** an outbox row in **one local transaction**, so the event can't be lost.
2. The outbox relay publishes `OrderPlaced` to the broker (possibly twice after a crash).
3. Payment consumes it, runs the **duplicate check** (eventId in `processed_events`, unique `orderId` in `payments`), and charges Stripe with **idempotency key = orderId**.
4. Payment publishes `PaymentSucceeded`, ideally through its own outbox (same reason as step 1).
5. Order marks the order `PAID`; Shipping and Notification react independently. Each consumer has its own duplicate check (no double shipments, no double emails).

**Pattern to remember:** every **producer** uses an outbox, and every **consumer** is idempotent. The failure path (`PaymentFailed` → `OrderCancelled` → stock released) follows the same shape.

---

## 4. Comparison of A, B and C

| Criterion | A – Modular monolith | B – Microservices (sync REST) | C – Event-driven |
|---|---|---|---|
| **Difficulty to build** | Low | Medium–high | High |
| **Operations** (deploy, monitor) | One app + one DB | Many services, gateway, discovery, tracing | Like B **+ broker** as critical infrastructure |
| **Consistency** | Strong (ACID inside the app); only payment needs the pattern from Q1 | No shared transaction; checkout coordinated through API calls | **Eventual**; sagas + compensations |
| **When something fails** | A crash takes down the whole app (unless replicated); a bug in one module affects all | Failure stays isolated per service, but **sync chains fail together** (Q4); needs timeouts and circuit breakers | Services can be down temporarily; events wait in the broker and are processed later. New risks: duplicates, lost events, wrong order (Q5) |
| **Scalability** | Whole app scales as one (X-axis) | Per service (e.g. scale only Catalog) | Per service, plus buffering of load spikes by the broker |
| **Fits "distributed"?** | Weakly; only through replication (Q2) | Yes, clearly | Yes, the most "distributed" |
| **Testing & debugging** | Easy, one process, one log | Harder: integration tests, tracing across calls | Hardest: timing-dependent bugs, needs correlation IDs and tracing |
| **Checkout pain point** | Dual write with Stripe (Q1) | Availability of the call chain (Q3–Q4) | Outbox, idempotency, saga compensations (Q5–Q6) |
| **Best when** | Small team, small domain, fast delivery | Several teams, parts with very different load | Many independent reactions to business events, high resilience needs |

### Recommendation for CDC

**Pick: pure B, microservices with synchronous REST and a small number of services.**

*(An earlier draft recommended a B+C hybrid. It was dropped because it needs **both** REST and a broker with outboxes, so it is more infrastructure than pure B, not less. It was also not one of the three compared options.)*

**Why B:**
- It clearly satisfies the CDC requirement of a **distributed system**, which A does only weakly (Q2).
- Most stories are simple requests (browse, search, profile, cart, merchant CRUD), which fit **request–response** naturally.
- It avoids C's hardest problems (outbox, duplicate and reordered events, sagas; Q5), which a shop this small doesn't need.
- There is only one communication style to build, test and explain.

**Proposed services (keep it small):**
- **Auth/User**: register, login, profiles, roles (Customer/Merchant).
- **Catalog**: products, search, sorting, merchant price and CRUD operations.
- **Order**: cart **and** orders together, since their data changes together (deliberate boundary decision).
- **Payment**: wraps Stripe (pattern from Q1).
- **Shipping/Notification**: package info, emails, contact form.

**Handling B's weak points without a broker:**
- **Catalog down at checkout (Q4)**: run 2+ Catalog instances, use timeouts and a circuit breaker, and fail **before** payment with the cart kept. Optionally honour a recent cart price snapshot (a business decision).
- **Duplicate charges**: Stripe idempotency key = orderId, plus a unique `orderId` in the `payments` table.
- **Shipping/Notification must not block checkout**: Order calls them **after** marking the order `PAID`. If a call fails, a status field (`shippingRequested = false`) and a small retry job in Order try again later. Checkout already succeeded, so this is a background task, not a failure.
- **Tracing**: an orderId/traceId passed in an HTTP header, centralised logs.

**Alternative answer**: if the teacher accepts replication as "distributed", a **horizontally scaled modular monolith (A)** is the simplest correct solution.
