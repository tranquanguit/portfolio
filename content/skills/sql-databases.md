---
title: SQL & Databases
slug: sql-databases
category: Integration & Data
icon: ⌗
short: SQL
level: 90
years: 4
summary: The one skill every part of my work rests on — Open SQL in ABAP, T-SQL on SQL Server, PL/SQL on Oracle, and SQLScript on HANA.
tags: [Open SQL, T-SQL, PL/SQL, SQLScript, SAP HANA, SQL Server, Oracle, Query Tuning]
featured: true
---

## Four dialects, one skill

| Dialect | Where |
| --- | --- |
| **Open SQL** | ABAP, across every SAP project |
| **SQLScript** | AMDP and CDS on SAP HANA |
| **T-SQL** | MS SQL Server — the Acecook warehouse |
| **PL/SQL** | Oracle — as a source system |

The syntax differs; the thinking does not. Set-based operations, correct joins, indexes that match access patterns, and an execution plan you have actually looked at.

## What I actually care about

**Think in sets.** The instinct to loop is the single most expensive habit a developer brings to SQL. Almost anything expressed as a loop over rows is expressible — and dramatically faster — as one statement over a set.

**Read the execution plan.** Not occasionally. Any time a query matters. The plan tells you whether your index is being used, where the row estimate went wrong, and which join is doing the damage. Guessing at query performance is a waste of everyone's afternoon.

**Selectivity beats cleverness.** The fastest query is the one that reads the fewest rows. Restrictive predicates, useful indexes, and a selection screen that does not default to "everything".

**Know your storage model.** HANA is columnar: selecting four fields instead of forty is not a small optimization, it is a different amount of work. SQL Server row-store rewards different choices. The same query can be well or badly written depending on where it runs.

**NULL is not a value.** It is the absence of one, and it does not behave like a value in comparisons, aggregates or joins. Most subtly wrong query results I have debugged trace back to this.

## Habits

- Explicit column lists, never `SELECT *`.
- Explicit `JOIN` syntax, never comma-joins with conditions in `WHERE`.
- CTEs to make a complex query readable in the order a person reads it.
- Comment the *why* of a non-obvious predicate. The `AND` clause that looks redundant is usually load-bearing.

> **To expand:** query-tuning walkthroughs on HANA and SQL Server side by side.
