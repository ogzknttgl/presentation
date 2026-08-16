# HERMES API DESIGN PROTOCOL

> Practical API design rules for Hermes when creating, reviewing, extending, or migrating APIs.
>
> Inspired by Sean Goedecke's “Everything I know about good API design”, adapted into an engineering execution protocol.

---

## 0. PURPOSE

This protocol governs API design decisions.

The objective is not to produce “clever” APIs.

The objective is to produce APIs that are:

```text
familiar
stable
safe to consume
easy to adopt
hard to misuse
operationally survivable
```

This protocol complements:

```text
HERMES_PROJECT_OS.md
PROJECT_BOOTSTRAP.md
ISSUE_PROTOCOL.md
EVALUATION_PROTOCOL.md
MEMORY_POLICY.md
```

---

# 1. PRIME DIRECTIVE

Good APIs should be boring.

Consumers should spend as little time as possible learning the interface.

Prefer familiar patterns over novelty.

A consumer should ideally be able to guess how common operations work before reading extensive documentation.

---

# 2. API DESIGN IS A BALANCE

Every API must balance:

```text
SIMPLICITY
vs
LONG-TERM FLEXIBILITY
```

Do not add abstraction merely because future changes might happen.

Do not design an interface that is unnecessarily rigid if change is clearly likely.

Prefer the simplest interface that preserves important future options.

---

# 3. WE DO NOT BREAK USERSPACE

For public APIs, compatibility is a primary obligation.

Do not break downstream consumers for aesthetic cleanup.

Avoid changing:

```text
existing field names
existing field types
existing response structure
existing required request fields
existing endpoint semantics
```

Avoid removing existing behavior unless a migration strategy exists.

---

# 4. ADDITIVE CHANGE FIRST

Prefer additive changes.

Examples:

```text
new optional response field
new endpoint
new optional request parameter
new capability
new enum value only when consumers can tolerate unknown values
```

Additive does not automatically mean safe.

Consider strict clients, generated SDKs, validation logic, and enum exhaustiveness.

But in general:

```text
ADD
before
CHANGE / REMOVE
```

---

# 5. BREAKING CHANGE TEST

Before changing an existing API contract ask:

```text
Can an existing consumer continue working without modifying code?
```

If NO:

```text
BREAKING CHANGE
```

Breaking changes require explicit justification.

---

# 6. VERSIONING IS A LAST RESORT

Use API versioning when the technical value of a breaking change is high enough to justify permanent maintenance complexity.

Possible strategies:

```text
/v1/resource
/v2/resource
```

or header/account-based version selection.

But remember:

```text
versioning creates parallel public contracts
parallel contracts require support
support creates long-term maintenance cost
```

Do not introduce a new API version merely to clean up awkward naming.

---

# 7. VERSION TRANSLATION

When multiple public versions exist, prefer:

```text
PUBLIC VERSION
↓
SERIALIZATION / TRANSLATION LAYER
↓
SHARED BUSINESS LOGIC
```

Avoid duplicating entire business implementations per API version.

Accept that some version-specific behavior may still leak into core logic.

---

# 8. PRODUCT MODEL FIRST

An API usually reflects the underlying product model.

If the product/domain model is confusing, the API will often expose that confusion.

Before inventing complex API workarounds ask:

```text
Is the real problem the underlying system model?
```

Do not expose accidental internal storage structure directly to consumers.

---

# 9. HIDE INTERNAL IMPLEMENTATION COMPLEXITY

Consumers should not need to understand:

```text
internal linked structures
internal queue topology
database layout
background job implementation
service boundaries
storage quirks
```

unless those concepts are genuinely part of the product.

Translate internal complexity into a consumer-friendly interface where practical.

---

# 10. DESIGN FOR THE CONSUMER

Do not assume every API consumer is an expert engineer.

Potential consumers include:

```text
professional engineers
students
analysts
product managers
sales engineers
hobbyists
automation scripts
internal tools
```

Reduce onboarding friction.

---

# 11. AUTHENTICATION SHOULD MATCH THE AUDIENCE

For public developer-facing APIs, support a simple programmatic authentication mechanism when security requirements allow it.

Examples:

```text
API key
personal access token
service token
```

Use more complex mechanisms such as OAuth when the use case requires:

```text
delegated access
user authorization
fine-grained scopes
short-lived credentials
```

Do not force an OAuth-style flow onto a simple server-to-server script without a reason.

---

# 12. INTERNAL API EXCEPTION

Internal APIs have different consumers.

You may tolerate:

```text
more complex authentication
coordinated breaking changes
tighter coupling
```

when all consumers are controlled by the same organization.

But internal APIs still require:

```text
reliability
clear contracts
safe retries
operational protection
```

Internal does not mean consequence-free.

---

# 13. RETRIES ARE NORMAL

Network calls fail.

Possible states after a timeout or 5xx include:

```text
operation never started
operation partially executed
operation completed but response was lost
```

Design action-taking APIs with retries in mind.

---

# 14. IDEMPOTENCY

For create/action operations where duplicate execution is harmful, support idempotency.

Concept:

```text
CLIENT SENDS:
request + idempotency key

SERVER:
seen key?
    YES → return prior result / do not duplicate
    NO  → execute and record key
```

Important cases include:

```text
payments
orders
messages
resource creation
external side effects
high-value actions
```

---

# 15. IDEMPOTENCY STORAGE

Storage depends on risk.

Possible approaches:

```text
database record
dedicated idempotency table
resource-level unique key
transactional store
key/value store
```

For high-risk operations, prefer a design that coordinates idempotency state and business state safely.

Do not rely on a non-transactionally coordinated cache for critical financial or irreversible operations without understanding the failure modes.

---

# 16. IDEMPOTENCY SCOPE

Not every endpoint needs an idempotency key.

Usually unnecessary for:

```text
GET
pure reads
safe deterministic lookups
resource-ID-scoped deletes
```

Consider idempotency for:

```text
POST create
POST action
async job creation
external side effects
financial operations
```

---

# 17. RATE LIMIT EVERYTHING EXPOSED TO CODE

Humans click slowly.

Code does not.

Any public API can be called far faster than its UI equivalent.

Therefore evaluate:

```text
request frequency
backend cost
fan-out
database cost
external calls
queue pressure
memory usage
```

---

# 18. EXPENSIVE OPERATIONS NEED TIGHTER LIMITS

Rate limits should reflect cost.

Example:

```text
cheap GET
→ relatively generous limit

bulk export
→ stricter limit

fan-out notification
→ much stricter limit
```

Do not apply one arbitrary rate limit to every endpoint if costs differ materially.

---

# 19. PROVIDE BACKOFF SIGNALS

Return useful rate-limit metadata.

Examples:

```text
Retry-After
remaining quota
reset time
```

Clients need enough information to behave responsibly.

---

# 20. KILLSWITCH / CUSTOMER ISOLATION

For APIs capable of creating serious backend load, preserve operational controls.

Examples:

```text
disable API access for one customer
temporarily block one integration
throttle one endpoint
disable expensive functionality
```

Do not design an API that cannot be contained during an incident.

---

# 21. PAGINATE LARGE COLLECTIONS

Never assume a collection will remain small.

Avoid:

```text
SELECT *
→ serialize entire collection
→ return everything
```

when datasets may become large.

---

# 22. OFFSET PAGINATION

Offset/page pagination is acceptable when datasets are bounded or relatively small.

Examples:

```text
?page=2
?offset=100
```

Advantages:

```text
simple
familiar
easy to implement
```

Limitations:

```text
large offsets become expensive
records can shift between pages
scaling is weaker
```

---

# 23. CURSOR PAGINATION

Prefer cursor-based pagination when collections may become very large.

Example:

```text
GET /tickets?cursor=abc123
```

Server conceptually executes:

```text
WHERE sort_key > cursor
ORDER BY sort_key
LIMIT N
```

Cursor pagination avoids increasingly expensive deep offsets when implemented on an appropriate indexed ordering.

---

# 24. PAGINATION RESPONSE

Prefer returning navigation metadata.

Example:

```json
{
  "items": [],
  "next_cursor": "abc123"
}
```

Do not require clients to reconstruct server pagination rules when the server can explicitly provide the next token.

---

# 25. CURSOR REQUIREMENTS

A robust cursor requires:

```text
stable ordering
deterministic ordering
indexed ordering where practical
well-defined tie breaking
opaque representation when useful
```

Do not expose an unstable cursor over a non-deterministic sort.

---

# 26. EXPENSIVE FIELDS SHOULD BE OPTIONAL

If a field requires expensive computation or additional service calls, do not necessarily return it by default.

Possible designs:

```text
?include_subscription=true
?include=posts,subscription
```

Default responses should remain cheap and predictable.

---

# 27. CONTROL RESPONSE EXPANSION

Use optional expansion for:

```text
associated objects
computed statistics
remote-service data
large nested collections
expensive aggregates
```

But prevent pathological expansions that can explode backend cost.

---

# 28. GRAPHQL IS A TRADEOFF, NOT A DEFAULT

Do not introduce GraphQL simply because response flexibility is desirable.

Evaluate:

```text
consumer expertise
query flexibility requirements
caching complexity
backend implementation complexity
authorization complexity
cost control
observability
N+1 risks
```

REST + explicit include/expand parameters may be simpler.

Use GraphQL where its flexibility materially outweighs its operational and cognitive costs.

---

# 29. API SHAPE SHOULD BE PREDICTABLE

Prefer consistent patterns across endpoints.

Examples:

```text
GET    /users/{id}
GET    /users
POST   /users
PATCH  /users/{id}
DELETE /users/{id}
```

Do not invent new interaction grammar for each resource.

Consistency reduces documentation burden.

---

# 30. RESOURCE NAMING

Prefer domain language over implementation language.

Good:

```text
/users
/orders
/issues
/reports
```

Avoid exposing internal names such as:

```text
/user_entity_records
/order_db_rows
/report_worker_objects
```

unless those concepts are actually public domain concepts.

---

# 31. ERRORS MUST BE ACTIONABLE

Error responses should help clients decide:

```text
fix request
retry
wait
authenticate
request permission
contact support
stop permanently
```

Prefer stable error codes plus human-readable messages.

Example:

```json
{
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Too many export requests.",
    "retry_after_seconds": 30
  }
}
```

---

# 32. DISTINGUISH RETRIABLE AND NON-RETRIABLE FAILURE

Clients should be able to reason about:

```text
validation failure
authentication failure
authorization failure
not found
conflict
rate limit
temporary server error
permanent server error
```

Do not return generic 500 responses for predictable client mistakes.

---

# 33. ASYNC OPERATIONS

If a request cannot reasonably complete within normal request latency, consider asynchronous jobs.

Example:

```text
POST /exports
→ 202 Accepted
→ job_id

GET /exports/{job_id}
→ status
```

Use async APIs for genuinely long-running operations.

Do not turn normal CRUD into background jobs merely because the backend design is awkward.

---

# 34. BULK OPERATIONS

When consumers must process large numbers of resources, consider explicit bulk endpoints.

But evaluate:

```text
partial failure semantics
idempotency
transaction boundaries
rate limits
payload size
timeout behavior
```

A bulk endpoint should be operationally safer than thousands of naive individual calls.

---

# 35. API EVOLUTION CHECKLIST

Before modifying an existing API ask:

```text
Is this additive?
Could existing clients break?
Could strict clients reject this?
Does an SDK need regeneration?
Does an enum expansion break exhaustive consumers?
Does pagination behavior change?
Does authentication behavior change?
Does error behavior change?
Does retry behavior change?
Does ordering change?
```

---

# 36. PUBLIC API REVIEW

For public API changes, independently review:

```text
compatibility
adoption friction
documentation
SDK impact
migration path
rate limiting
idempotency
observability
deprecation
```

Public APIs deserve a higher compatibility threshold.

---

# 37. INTERNAL API REVIEW

For internal API changes review:

```text
known consumers
deployment order
mixed-version operation
rollback
service ownership
contract tests
```

A coordinated breaking change may be acceptable only if all affected consumers are controlled and migrated safely.

---

# 38. CONTRACT TESTING

When practical, encode API expectations in:

```text
OpenAPI
schema tests
consumer-driven contracts
integration tests
serialization tests
```

Executable contracts are stronger than prose-only rules.

---

# 39. DOCUMENTATION

Documentation should prioritize:

```text
authentication
first successful request
common examples
error behavior
pagination
rate limits
idempotency
versioning
deprecation
```

Optimize for the user getting from zero to a working integration quickly.

---

# 40. DESIGN REVIEW QUESTIONS

Before accepting a new endpoint ask:

```text
Can a consumer guess how this works?

Does this expose an internal implementation accident?

Can it evolve without breaking consumers?

What happens on retry?

What happens under abuse?

What happens at 100x the current data volume?

What happens if an expensive field is requested repeatedly?

Can the API be throttled or disabled during an incident?

How does the consumer know what to do after an error?
```

---

# 41. ANTI-PATTERNS

Avoid:

```text
clever endpoint naming
breaking cleanup
unbounded list endpoints
arbitrary expensive queries
action endpoints with unsafe retry behavior
one-size-fits-all rate limits
internal storage leaking into public contracts
mandatory expensive response fields
versioning for aesthetic reasons
GraphQL by default
generic 500 errors for predictable conditions
```

---

# 42. HERMES FEATURE INTEGRATION

When an issue or feature affects an API, Hermes must automatically invoke this protocol.

Flow:

```text
ISSUE / FEATURE
↓
API IMPACT DETECTED
↓
API DESIGN PROTOCOL
↓
COMPATIBILITY CHECK
↓
RETRY / IDEMPOTENCY CHECK
↓
SCALE / PAGINATION CHECK
↓
RATE-LIMIT CHECK
↓
IMPLEMENT
↓
CONTRACT TEST
↓
REVIEW
```

---

# 43. API CHANGE CLASSIFICATION

Classify API changes as:

```text
ADDITIVE_COMPATIBLE
BEHAVIORAL_COMPATIBLE
POTENTIALLY_BREAKING
BREAKING
```

Do not treat API work like ordinary internal refactoring.

---

# 44. DEPRECATION POLICY

When removing public behavior:

```text
announce
↓
document replacement
↓
provide migration path
↓
measure remaining usage
↓
allow sufficient migration time
↓
remove only when justified
```

Do not silently remove public behavior.

---

# 45. OBSERVABILITY

For important APIs track:

```text
request rate
latency
error rate
status-code distribution
rate-limit events
expensive endpoint usage
timeouts
retry patterns
customer-specific load
```

Operational data should influence future design.

---

# 46. API DESIGN DEFINITION OF DONE

For meaningful API work:

```text
[ ] consumer-facing behavior is clear
[ ] compatibility reviewed
[ ] request/response contract defined
[ ] failure semantics defined
[ ] retry behavior considered
[ ] idempotency considered
[ ] rate limiting considered
[ ] pagination considered for collections
[ ] expensive fields considered
[ ] authentication/authorization reviewed
[ ] contract tests added or updated
[ ] documentation updated where needed
[ ] diff contains no unrelated contract changes
```

---

# 47. CORE PRINCIPLE

A good API is not impressive.

A good API disappears into the consumer's work.

Prefer:

```text
predictability
compatibility
safety
simplicity
operational control
```

over cleverness.
