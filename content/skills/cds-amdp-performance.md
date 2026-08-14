---
title: CDS Views, AMDP & Performance
slug: cds-amdp-performance
category: SAP Development
icon: ⚡
short: Performance
level: 85
years: 3
summary: Code-to-data optimization on SAP HANA — pushing logic down with CDS views and AMDP, and rescuing reports that could not survive production volumes.
tags: [CDS Views, AMDP, SQLScript, Code Pushdown, Parallel Processing, SQL Trace]
featured: true
---

## Why this became a specialty

Because reports I had written broke. On a development system with a few thousand records everything is fast. Against production volume — hundreds of thousands of documents, or 300 million rows in a warehouse — the same code is unusable. Learning to fix that properly, rather than adding indexes and hoping, was the biggest step up in my second year.

## The principle: code to data

Classic ABAP reads data from the database into the application server and processes it there. On HANA that is backwards. The database is fast, it is columnar, it parallelises, and moving a million rows across to the application layer to filter them is pure waste.

**Move the work to the data.** Aggregate, join, filter and calculate in the database; return only what the report displays.

## The tools, in the order I reach for them

**1. CDS views.** The default. Joins, aggregation, calculated fields and associations, defined declaratively and reusable across reports, Fiori apps and analytics. Most performance problems I have met were solved at this level.

**2. AMDP.** When the logic genuinely needs procedural SQLScript — multi-step transformations, intermediate result sets, loops over sets that a single view cannot express. Powerful, but it puts database-specific code in your ABAP class, so it should be a deliberate choice.

**3. Parallel processing.** When the work is genuinely partitionable and the volume justifies the coordination cost.

## How I actually diagnose

Measurement before theory, always:

- **SQL Trace (ST05)** — which statement, how often, how long. The answer is usually "this one, 40,000 times".
- **ABAP Runtime Analysis (SAT)** — where the time goes when it is not the database.
- **HANA plan visualisation** — for a CDS view or AMDP that is slow for a non-obvious reason.

Nine times out of ten the finding is the same shape: a database read inside a loop, or a select without a restrictive enough where clause.

## Rules I follow

- Never `SELECT *` when you need four fields — this matters far more on a columnar store than a row store.
- Guard `FOR ALL ENTRIES` against an empty driver table.
- Aggregate in the database, not with `LOOP ... AT ... SUM`.
- Sorted or hashed internal tables for lookups inside loops.
- Restrictive selection screen defaults — the fastest query is the one that reads less.

> **To expand:** a before-and-after case study with real numbers from the HURC1 ticket-sales report.
