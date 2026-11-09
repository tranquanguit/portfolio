---
title: Inventory Is a Ledger, Not a Number
slug: inventory-as-a-ledger
topic: SAP & ERP
date: 2026
status: draft
publishedOn: This site
summary: Why I build stock as a derived sum of immutable transactions instead of a mutable quantity field — an ERP habit that small systems almost always skip, and regret.
tags: [Inventory, ERP Design, Data Modelling, Dropship Hub, SAP MM]
featured: true
---

## Two ways to store stock

**The obvious way.** A `quantity_on_hand` column on the product. A receipt adds to it, an issue subtracts from it. One row, one read, fast.

**The ERP way.** A table of movements — receipts, issues, adjustments, transfers — each immutable. Stock on hand is the sum of them.

Almost every small system picks the first. Almost every ERP picks the second. The reason is worth understanding, because it is not about performance.

## What the mutable number cannot do

It cannot answer **"why"**.

Stock says 48. The warehouse counts 45. Where did the three go? With a quantity column the honest answer is *we don't know* — the history was overwritten each time the number changed. You can look at order records and try to reconstruct it, which is exactly the archaeology the ledger was supposed to prevent.

It also fails under concurrency in ways that are hard to see. Two processes reading 48, each subtracting 5, each writing their result: the final value is 43 and one movement has vanished. You can solve this with locking — and now you have a lock on the hottest row in the system.

With a ledger, both processes insert. Nothing is lost, because nothing is overwritten.

## What it costs

A join and an aggregate where the naive design has a single column read. That is a real cost and it is worth being honest about it.

The usual answer is a **snapshot**: a periodically materialised balance plus the movements since. SAP does a version of this. It keeps the audit trail intact while making the common read cheap — and crucially, the snapshot is derived, so if it is ever wrong you rebuild it from the ledger rather than guessing.

## Where I applied it

[Dropship Hub](products/dropship-hub.html) is built this way. Every movement is a transaction; quantity on hand is derived. Paired with bill-of-materials explosion, so an assembled product consumes its components correctly, and an explicit order state machine, so stock-affecting transitions cannot happen out of order.

None of that is novel. It is standard ERP thinking applied to a small business system — which is precisely the gap I keep seeing. Tools built for small businesses tend to assume small businesses have simple problems. They have the same problems, with fewer people to absorb the consequences.

## The general lesson

**Store what happened, derive what is true.**

It applies well beyond inventory: account balances, document status, approval state. The event is the fact. Everything else is a projection you can rebuild.

> **Draft.** I plan to add the snapshot design and the concurrency tests.
