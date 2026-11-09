---
title: Microsoft Fabric Data Platform — PB15, FPT IS HCM
slug: fabric-data-platform
org: fis
client: FPT IS HCM — internal
period: 02/2025 – 04/2026
start: 2025-02
end: 2026-04
role: Team Lead — Data Platform
featured: true
image:
summary: Led the team that brought Microsoft Fabric into FPT IS HCM — a medallion Lakehouse with Data Pipelines, Dataflow Gen2 and Notebooks serving Power BI, plus internal training and presales support.
tags: [MS Fabric, Lakehouse, Medallion, Dataflow Gen2, Notebooks, Data Pipelines, Power BI, Team Lead]
highlights:
  - Led the team that researched and adopted Microsoft Fabric (Data Pipelines, Dataflow Gen2, Notebooks, Lakehouse) and trained internal members on the platform.
  - Built an end-to-end ETL flow from the internal application database through staging and enrichment layers using a medallion architecture, serving Power BI dashboards.
  - Supported presales for customers evaluating Fabric-based data platforms.
---

## Context

This one had no customer and no deadline, which made it harder rather than easier.

After the Acecook warehouse shipped on SQL Server and SSIS, the obvious question was what the next platform looks like. Microsoft Fabric was new, customers had started asking about it, and nobody in the department had used it. I led the group that found out.

## Medallion, in practice

We built an end-to-end flow from the internal application database through to Power BI, structured as a **medallion architecture**:

- **Bronze** — raw, as it arrived, nothing cleaned.
- **Silver** — conformed and cleansed, the layer where business rules live.
- **Gold** — enriched and modelled for the questions people actually ask.

If that sounds like the staging / cleansed / presentation split I used on SQL Server, it is. The names change; the reason does not. What changes on Fabric is where it runs: a **Lakehouse** rather than a relational warehouse, with **Data Pipelines** for orchestration, **Dataflow Gen2** for transformation that suits a low-code approach, and **Notebooks** where the logic needs real code.

## Choosing between three tools that all work

The genuine difficulty with Fabric is not learning any one component — it is that Pipelines, Dataflow Gen2 and Notebooks overlap. You can solve the same problem three ways.

Where I landed:

- **Data Pipelines** for movement and orchestration — getting data from A to B on a schedule.
- **Dataflow Gen2** for transformations a data analyst should be able to read and change without asking an engineer.
- **Notebooks** when the logic is genuinely complex, needs testing, or has to be version-controlled like code.

The failure mode is using Notebooks for everything because you are comfortable in Python. It works, and it quietly makes the whole platform un-maintainable by anyone who is not you.

## Leading an adoption rather than a project

A customer project tells you when you are done. An internal initiative does not, so I set the definition myself: **the team can build on it without me, and we can stand in front of a customer and answer honestly.**

That meant training was the deliverable, not a side effect. I ran sessions for internal members, and we supported **presales** for customers evaluating Fabric — which is the real exam. A customer asking "why Fabric and not Databricks, and what does it cost at our volume" finds out immediately whether you learned the platform or learned the marketing.

> **To expand:** the Fabric vs. SQL Server + SSIS comparison I use with customers, and what I would warn a team about before they start.
