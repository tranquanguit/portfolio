---
title: SAP BTP & Clean Core Architecture
slug: btp-architecture
category: SAP Development
icon: ⬡
short: BTP Arch
radar: true
level: 80
years: 1.5
summary: Designing extensions on SAP Business Technology Platform — side-by-side versus in-stack, Integration Suite, Event Mesh, and the clean-core decisions that make an upgrade cheap instead of expensive.
tags: [SAP BTP, Clean Core, Side-by-Side Extensibility, ABAP Cloud, Integration Suite, Event Mesh, CAP]
featured: true
---

## Where I use it

Daily, on SimpleMDG — a master data governance product that *lives* on SAP BTP and reaches into ten different customer S/4HANA landscapes. Certified as **SAP Certified Professional — Solution Architect, SAP BTP** (P_BTPA), April 2026.

## The question clean core actually asks

It is easy to say "don't modify standard SAP". The useful question is the follow-up: **then where does this logic go?**

The BTP model gives three real answers, and choosing between them is most of the architecture work:

**In-stack, with ABAP Cloud.** When the logic genuinely belongs to the business object and needs to run inside the transaction. Released APIs and released extension points only — the compiler enforces what used to be a code-review argument.

**Side-by-side, on BTP.** When the capability has its own lifecycle, its own release cadence, or has to serve more than one backend. SimpleMDG is exactly this case: a governance product that cannot live inside any one customer's core.

**Integration, in between.** When two systems each legitimately own their part and the problem is getting data across the gap safely.

The failure I see most often is putting something in-stack because that is where the developer is comfortable, and discovering at the next upgrade that it was a lifecycle decision made by accident.

## Synchronous or event-driven

A distinction I apply constantly:

- **Synchronous call** when the caller cannot continue without the answer.
- **Event, via Event Mesh** when something happened that others may care about, and none of them should block it.

Master data governance leans heavily towards the second. A business partner being approved is an event — several systems want to know, and the approval should not wait for any of them.

## What building a product taught me that projects did not

A project has one landscape. A product has ten, and the architecture has to survive all of them.

That changes the defaults: fewer assumptions about configuration, no reliance on a field being filled because this customer happens to fill it, and a hard rule that anything customer-specific is configuration rather than code. It also means **rollout is part of the architecture** — transport strategy, Basis prerequisites, and what happens when a customer is two releases behind.

> **To expand:** the side-by-side vs. in-stack decision tree, with a worked example.
