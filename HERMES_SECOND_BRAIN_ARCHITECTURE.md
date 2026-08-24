# HERMES SECOND BRAIN ARCHITECTURE
## Persistent Context, Knowledge, Memory & Obsidian Reference Architecture

> **Role:** Companion document to `HERMES_ENGINEERING_CONSTITUTION_FINAL.md`
>
> **Purpose:** Define how Hermes should capture, structure, retrieve, use, update, and maintain persistent knowledge across sessions without turning every prompt into a context dump.
>
> The engineering constitution defines **how Hermes engineers software**.
>
> This document defines **how Hermes remembers and retrieves what it needs to engineer well**.

---

# 1. CORE PRINCIPLE

Hermes should not depend on a single conversation window.

The knowledge system must survive:

- sessions,
- model changes,
- context-window limits,
- restarts,
- team handoffs,
- long-running projects.

The desired loop is:

```text
RAW INFORMATION
      ↓
STRUCTURED KNOWLEDGE
      ↓
RETRIEVAL
      ↓
ACTIVE CONTEXT
      ↓
WORK / OUTPUT
      ↓
REVIEW
      ↓
NEW DURABLE KNOWLEDGE
      └──────────────→ STRUCTURED KNOWLEDGE
```

The system should compound in value over time.

---

# 2. DESIGN PRINCIPLES

## 2.1 Persistent Memory

Important context must survive individual chat sessions.

Examples:

- architecture decisions,
- engineering preferences,
- active project goals,
- constraints,
- important people/teams,
- stable environment facts,
- lessons from incidents,
- reusable implementation knowledge.

Do not rely on conversational recall for durable engineering truth.

---

## 2.2 Separation of Concerns

Keep different kinds of information in different layers.

```text
RAW
→ immutable source material

WIKI
→ structured, linked knowledge

OUTPUT
→ generated artifacts

CTX
→ reusable working context and instructions

MEM
→ durable identity, goals and system memory
```

Do not mix all information into one giant folder.

---

## 2.3 Connected Knowledge

Knowledge should reference related knowledge.

Examples:

```text
Service
→ API
→ database table
→ architecture decision
→ incident
→ runbook
```

or:

```text
Project
→ goals
→ current architecture
→ open decisions
→ related literature
→ implementation plan
```

Prefer explicit links over isolated notes.

---

## 2.4 Personalization

The system should preserve stable preferences and working conventions where useful.

Examples:

- preferred engineering style,
- preferred technology boundaries,
- reporting format,
- recurring project constraints,
- tool conventions.

Personalization should improve future work without polluting technical truth.

Keep preferences separate from authoritative project facts.

---

## 2.5 Compounding Value

Every useful session should have the potential to improve future sessions.

But not every conversation should be saved.

Store only information with durable value.

The desired effect is:

```text
More useful sources
      ↓
Better structured knowledge
      ↓
Better retrieval
      ↓
Better context
      ↓
Better outputs
      ↓
Better durable knowledge
```

---

# 3. REFERENCE ARCHITECTURE

```text
                         ┌──────────────────────┐
                         │        RAW           │
                         │ immutable sources    │
                         └──────────┬───────────┘
                                    │
                              ingest / extract
                                    │
                         ┌──────────▼───────────┐
                         │        WIKI          │
                         │ structured knowledge │
                         └──────┬─────┬─────────┘
                                │     │
                    ┌───────────┘     └──────────────┐
                    │                                │
             ┌──────▼──────┐                  ┌──────▼──────┐
             │  RETRIEVE   │                  │   OUTPUT    │
             │ find context│                  │ artifacts   │
             └──────┬──────┘                  └──────┬──────┘
                    │                                │
                    └──────────────┬─────────────────┘
                                   │
                            ┌──────▼──────┐
                            │    USE      │
                            │ active work │
                            └──────┬──────┘
                                   │
                            ┌──────▼──────┐
                            │     CTX     │
                            │ rules /     │
                            │ templates   │
                            └──────┬──────┘
                                   │
                            ┌──────▼──────┐
                            │     MEM     │
                            │ durable     │
                            │ memory      │
                            └──────┬──────┘
                                   │
                              review/update
                                   │
                                   └──────────────→ WIKI / MEM
```

---

# 4. KNOWLEDGE LAYERS

Recommended structure:

```text
second-brain/
│
├── raw/
│   ├── articles/
│   ├── pdfs/
│   ├── screenshots/
│   ├── transcripts/
│   ├── meeting-notes/
│   ├── voice/
│   ├── web-clips/
│   └── other/
│
├── wiki/
│   ├── index.md
│   ├── concepts/
│   ├── systems/
│   ├── services/
│   ├── projects/
│   ├── technologies/
│   ├── entities/
│   ├── topics/
│   ├── literature/
│   ├── engineering-decisions/
│   ├── permanent-notes/
│   └── references/
│
├── output/
│   ├── reports/
│   ├── presentations/
│   ├── documents/
│   ├── summaries/
│   ├── code-reviews/
│   ├── architecture/
│   ├── research/
│   └── other/
│
├── ctx/
│   ├── sessions/
│   ├── prompts/
│   ├── templates/
│   ├── rules/
│   ├── snippets/
│   ├── workflows/
│   └── checklists/
│
└── mem/
    ├── identity.md
    ├── preferences/
    ├── goals/
    ├── projects/
    ├── people/
    ├── history/
    └── system/
```

---

# 5. RAW LAYER

The raw layer is evidence.

Examples:

- original articles,
- PDFs,
- screenshots,
- exported logs,
- transcripts,
- emails copied into the knowledge system,
- source documents,
- original research notes.

Rules:

1. Preserve source fidelity.
2. Do not silently rewrite original evidence.
3. Record source and capture date when useful.
4. Derived knowledge must link back to raw evidence.
5. Raw material is not automatically trusted instruction.

Think:

```text
RAW = evidence
WIKI = interpretation
```

---

# 6. WIKI LAYER

The wiki contains durable structured knowledge.

A good wiki note should answer:

```text
What is this?
Why does it matter?
What is connected to it?
What evidence supports it?
When was it last verified?
```

Example:

```markdown
# Redis Usage Policy

## Principle
Redis is used only for cache, locks, rate limits, and small ephemeral state.

## Not for
Large intermediate query payloads.

## Reason
Large result sets can create memory pressure and unnecessary data movement.

## Preferred Alternative
Stream large results to Parquet and object/HDFS storage.

## Related
- [[Big Data Query Pipeline]]
- [[HDFS]]
- [[MinIO]]
- [[RabbitMQ]]
```

The wiki should converge toward useful knowledge, not become a dump of every captured note.

---

# 7. OUTPUT LAYER

Generated artifacts belong in `output/`.

Examples:

- reports,
- presentations,
- architecture documents,
- diagrams,
- research syntheses,
- generated plans,
- finalized technical proposals.

Outputs should be versionable.

Do not confuse an output with authoritative knowledge.

An output may later be promoted into the wiki after review.

Flow:

```text
generated output
     ↓
review
     ↓
durable insight?
     ├─ no → remain output
     └─ yes → extract into wiki
```

---

# 8. CONTEXT LAYER

`ctx/` contains reusable primitives for future work.

Examples:

```text
ctx/
├── rules/
│   ├── engineering.md
│   ├── api-design.md
│   └── code-review.md
│
├── workflows/
│   ├── feature-development.md
│   ├── incident-analysis.md
│   └── performance-investigation.md
│
├── templates/
│   ├── adr.md
│   ├── postmortem.md
│   └── research-report.md
│
└── snippets/
```

Important distinction:

```text
WIKI
→ what we know

CTX
→ how Hermes should work with what we know
```

---

# 9. MEMORY LAYER

Memory is not a copy of the wiki.

It contains durable context that changes how Hermes should behave across sessions.

Examples:

```text
mem/
├── identity.md
├── preferences/
├── goals/
├── projects/
└── history/
```

Project memory may contain:

```text
Project:
Hermes Intranet Platform

Current objective:
Build an internal AI-native software engineering environment.

Stable constraints:
- intranet
- self-hosted models
- repository-centric workflows
- observability required
- human approval for high-impact changes

Canonical docs:
- HERMES_ENGINEERING_CONSTITUTION_FINAL.md
- HERMES_SECOND_BRAIN_ARCHITECTURE.md
```

Do not store temporary debugging state as durable memory.

---

# 10. THREE TYPES OF MEMORY

Hermes should conceptually distinguish:

## Semantic Memory

Durable facts.

```text
"Service X uses PostgreSQL."
```

## Episodic Memory

Important prior events.

```text
"Incident 2026-08-12 involved retry amplification."
```

## Procedural Memory

How work is done.

```text
"For API changes run contract tests before merge."
```

Mapping:

```text
semantic
→ wiki/

episodic
→ wiki/incidents/ or mem/history/

procedural
→ ctx/workflows/ and ctx/rules/
```

---

# 11. RETRIEVAL ARCHITECTURE

Do not inject the whole second brain into every prompt.

Use layered retrieval.

```text
USER TASK
    ↓
Determine intent
    ↓
Retrieve canonical rules
    ↓
Retrieve project context
    ↓
Retrieve task-specific knowledge
    ↓
Retrieve raw evidence only if necessary
    ↓
Construct bounded active context
```

Recommended retrieval order:

```text
1. Canonical engineering rules
2. Active project context
3. Exact repository evidence
4. Relevant wiki notes
5. Historical decisions
6. Raw source material
```

Repository/runtime evidence can override stale knowledge notes.

---

# 12. HYBRID RETRIEVAL

For an intranet system, retrieval should not depend on vector similarity alone.

Use:

```text
Exact search
+
symbol/code search
+
metadata filters
+
links/graph relations
+
semantic/vector retrieval
```

Example:

```text
Query:
"Why did we stop using Redis for result transfer?"

Retrieve:
1. exact phrase matches,
2. ADR / architecture notes,
3. linked Big Data Pipeline note,
4. relevant prior incident,
5. semantic fallback.
```

The goal is not maximum recall.

The goal is **minimum sufficient authoritative context**.

---

# 13. CONNECTED KNOWLEDGE GRAPH

Represent meaningful relationships explicitly.

Possible relations:

```text
PROJECT
 ├── USES → TECHNOLOGY
 ├── OWNS → SERVICE
 ├── DEPENDS_ON → SERVICE
 ├── DECIDED_BY → ADR
 ├── EXPERIENCED → INCIDENT
 └── GOVERNED_BY → RULE
```

Example:

```text
Hermes Intranet
 ├── USES → FastAPI
 ├── USES → PostgreSQL
 ├── USES → Qdrant
 ├── GOVERNED_BY → Engineering Constitution
 └── HAS_MEMORY_ARCHITECTURE → Second Brain Architecture
```

Knowledge graph links can be simple Markdown/Obsidian links initially.

Do not introduce a dedicated graph database until a real need appears.

---

# 14. OBSIDIAN AS HUMAN KNOWLEDGE INTERFACE

Obsidian can serve as the human-readable knowledge workspace.

Recommended roles:

```text
Obsidian
→ editing
→ browsing
→ linking
→ human review
→ knowledge gardening

Qdrant / search index
→ machine retrieval

Filesystem / Git
→ canonical persistence
```

Do not treat a vector database as the source of truth.

The vector index is derivative.

Canonical truth should remain in readable/versionable files.

---

# 15. INDEXING PIPELINE

Example:

```text
Markdown / source files
       ↓
parse
       ↓
metadata extraction
       ↓
chunk
       ↓
embed
       ↓
index in Qdrant
```

Store metadata:

```json
{
  "path": "wiki/systems/query-pipeline.md",
  "title": "Big Data Query Pipeline",
  "type": "wiki",
  "project": "intranet",
  "updated_at": "2026-08-24",
  "authority": "canonical"
}
```

Retrieval should preserve source path so Hermes can inspect the original document.

---

# 16. INGEST AUTOMATION

Automation #1:

```text
CAPTURE
  ↓
EXTRACT
  ↓
CLASSIFY
  ↓
LINK
  ↓
ADD TO RAW
  ↓
OPTIONALLY PROMOTE TO WIKI
```

Never automatically convert every captured item into canonical knowledge.

Raw ingestion may be automatic.

Canonical promotion should require sufficient confidence or review.

---

# 17. WRITE AUTOMATION

Automation #2:

```text
RETRIEVE
  ↓
DRAFT
  ↓
VERIFY
  ↓
REFINE
  ↓
OUTPUT
```

Generated work should cite or link its source context internally when feasible.

---

# 18. MANAGE AUTOMATION

Automation #3:

```text
DECISION
  ↓
LINK TO PROJECT
  ↓
LINK TO SYSTEM
  ↓
TRACK STATUS
```

Examples:

- ADR approved,
- technology selected,
- architecture changed,
- project constraint added.

Durable decisions should not remain buried in chat.

---

# 19. REVIEW AUTOMATION

Automation #4:

```text
SUMMARIZE
  ↓
REFLECT
  ↓
EXTRACT DURABLE INSIGHTS
  ↓
UPDATE WIKI / MEMORY
```

Good candidates:

- completed project milestones,
- incidents,
- architecture decisions,
- repeated debugging lessons,
- recurring user preferences,
- important research synthesis.

---

# 20. MAINTENANCE AUTOMATION

Automation #5:

```text
PRUNE
  ↓
DE-DUPLICATE
  ↓
CHECK BROKEN LINKS
  ↓
CHECK STALE KNOWLEDGE
  ↓
MERGE DUPLICATES
  ↓
IMPROVE CONNECTIONS
```

A second brain without maintenance becomes a second junk drawer.

---

# 21. MEMORY WRITE POLICY

Before writing durable memory, ask:

```text
Will this still matter in future sessions?
Is it stable enough?
Does it change future behavior?
Is there already an authoritative record?
Is this personal preference or technical fact?
```

Do not persist:

- temporary errors,
- one-off commands,
- speculative ideas,
- transient status,
- unverified assumptions.

Persist:

- stable preferences,
- durable constraints,
- important decisions,
- verified system facts,
- repeated lessons,
- long-term goals.

---

# 22. KNOWLEDGE PROMOTION STATES

Useful states:

```text
RAW
→ REVIEWED
→ STRUCTURED
→ CANONICAL
→ SUPERSEDED
→ ARCHIVED
```

Not all knowledge has equal authority.

Add metadata where useful:

```yaml
status: canonical
verified: 2026-08-24
owner: platform-team
source:
  - docs/architecture/...
supersedes:
  - old-note.md
```

Hermes should prefer canonical and recently verified sources.

---

# 23. CONFLICT RESOLUTION

If sources disagree:

```text
Repository/runtime evidence
        >
Canonical architecture/ADR
        >
Verified wiki
        >
Reviewed notes
        >
Raw material
        >
Memory summary
```

Do not silently merge conflicting facts.

Surface conflict.

Example:

```text
Wiki says Redis is used for staging.
Current code writes directly to MinIO.

→ Treat code/runtime as current behavior.
→ Flag wiki as stale.
→ Update after verification.
```

---

# 24. TEMPORAL AWARENESS

Knowledge changes over time.

Store dates for volatile facts.

Examples:

```text
verified_at
valid_from
superseded_at
source_date
```

Hermes should avoid treating an old architecture note as permanently true.

---

# 25. PROJECT CONTEXT PACK

For each significant project, maintain a compact context pack.

Example:

```text
mem/projects/hermes-intranet.md
```

Contents:

```markdown
# Hermes Intranet

## Goal
...

## Current Architecture
...

## Constraints
...

## Canonical Documents
...

## Active Decisions
...

## Open Risks
...

## Related Systems
...

## Last Reviewed
...
```

This file should be compact.

It is an entry point, not a full history.

---

# 26. SESSION CONTEXT

Temporary session material belongs in:

```text
ctx/sessions/
```

Example:

```text
ctx/sessions/2026-08-24-hermes-graph-design.md
```

At session end:

```text
session
  ↓
extract durable insight?
  ├── yes → wiki / mem / ctx
  └── no → expire/archive
```

Do not automatically turn session transcripts into long-term memory.

---

# 27. CANONICAL DOCUMENT MAP

For the Hermes engineering environment:

```text
HERMES_ENGINEERING_CONSTITUTION_FINAL.md
→ engineering behavior and operating rules

HERMES_SECOND_BRAIN_ARCHITECTURE.md
→ persistent knowledge/context/memory architecture

AGENTS.md
→ short operational map into canonical docs

ARCHITECTURE.md
→ current system architecture

docs/design-decisions/
→ why important decisions were made

docs/runbooks/
→ operational procedures

docs/incidents/
→ production learning
```

---

# 28. AGENTS.md INTEGRATION

Recommended top-level `AGENTS.md`:

```markdown
# Hermes Repository Instructions

## Canonical Rules
Read:
- HERMES_ENGINEERING_CONSTITUTION_FINAL.md
- HERMES_SECOND_BRAIN_ARCHITECTURE.md

## Architecture
Read:
- ARCHITECTURE.md

## Build
...

## Test
...

## Knowledge System
Use:
- wiki/ for durable technical knowledge
- ctx/ for workflows/templates
- mem/ for durable project/user context
- raw/ for source material
- output/ for generated artifacts
```

Keep `AGENTS.md` small.

---

# 29. SECURITY AND PRIVACY

Persistent memory increases capability and risk.

Apply:

- access control,
- least privilege,
- audit logs,
- data classification,
- secret filtering,
- retention policies,
- encryption where required.

Never index secrets into semantic search.

Examples to exclude:

```text
passwords
private keys
API secrets
access tokens
sensitive production credentials
```

Memory should not become a credential store.

---

# 30. SECOND BRAIN OBSERVABILITY

Track:

```text
retrieval query
retrieved sources
source authority
retrieval scores
context size
used/not-used sources
memory writes
memory updates
stale-source warnings
```

Useful metrics:

```text
retrieval precision
unused-context rate
stale-note rate
duplicate-note rate
broken-link count
memory growth
canonical-document freshness
```

---

# 31. QUALITY CONTROL

A second brain should improve signal-to-noise ratio over time.

Bad growth:

```text
More files
→ more noise
→ worse retrieval
```

Desired growth:

```text
More verified knowledge
→ stronger links
→ better metadata
→ better retrieval
→ smaller active context
→ better decisions
```

Therefore:

> **Knowledge quality matters more than knowledge volume.**

---

# 32. COMPOUNDING LOOP

The complete loop:

```text
SOURCE
  ↓
CAPTURE
  ↓
RAW
  ↓
REVIEW
  ↓
WIKI
  ↓
INDEX
  ↓
RETRIEVE
  ↓
ACTIVE CONTEXT
  ↓
HERMES WORK
  ↓
OUTPUT
  ↓
EVALUATE
  ↓
NEW DURABLE INSIGHT
  ↓
WIKI / CTX / MEM
  ↓
MAINTAIN
  └──────────────→ better future retrieval
```

---

# 33. WHAT NOT TO DO

Avoid:

## Context Dumping

Loading all notes into every task.

## Memory Hoarding

Saving every conversation.

## Vector DB as Truth

Embeddings are an index, not canonical knowledge.

## Automatic Canonicalization

Captured information is not automatically correct.

## Duplicate Truth

Do not maintain the same fact independently in five files.

## Stale Memory

Old knowledge must be superseded or revalidated.

## Hidden Personalization

Preferences should not silently override technical constraints.

## Premature Graph Database

Obsidian links and metadata are enough until graph querying becomes a demonstrated need.

---

# 34. IMPLEMENTATION STAGES

## Stage 1 — Filesystem + Obsidian

```text
raw/
wiki/
output/
ctx/
mem/
```

Use Markdown, links, Git and manual review.

This should be the starting point.

---

## Stage 2 — Search Index

Add:

```text
full-text search
metadata search
```

---

## Stage 3 — Semantic Retrieval

Add:

```text
Qdrant
embeddings
hybrid retrieval
```

Canonical files remain the source of truth.

---

## Stage 4 — Automated Knowledge Gardening

Add scheduled:

```text
stale-note detection
duplicate detection
broken-link checks
index refresh
session-review suggestions
```

---

## Stage 5 — Knowledge Graph Only If Needed

Possible later additions:

```text
entity relations
dependency graph
cross-project graph queries
temporal graph
```

Do not add a graph database without concrete retrieval requirements.

---

# 35. FINAL RULES

1. **Persistent context should live outside the conversation window.**
2. **Raw evidence, structured knowledge, outputs, context primitives, and memory are different things.**
3. **Canonical knowledge must remain human-readable and versionable.**
4. **Obsidian/filesystem can be the source of truth; vector stores are derivative indexes.**
5. **Retrieve on demand rather than preload everything.**
6. **Store durable knowledge, not conversational noise.**
7. **Every durable claim should have provenance when practical.**
8. **Knowledge must be linked, reviewed, and maintained.**
9. **Stale knowledge is a reliability problem.**
10. **The system should improve future context quality with every useful cycle.**

---

# 36. PRIME DIRECTIVE

> **Do not build a memory system that remembers everything. Build a knowledge system that makes the right thing easy to retrieve at the right time.**

For Hermes:

```text
CAPTURE
→ STRUCTURE
→ LINK
→ RETRIEVE
→ USE
→ VERIFY
→ UPDATE
→ PRUNE
```

The purpose of the second brain is not infinite memory.

The purpose is **persistent, trustworthy, increasingly useful context**.
