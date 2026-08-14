---
title: Data Warehouse & Power BI — Acecook Vietnam
slug: acecook-data-warehouse
org: fis
client: Acecook Vietnam JSC
period: 02/2025 – 06/2025
start: 2025-02
end: 2025-06
role: Data Engineer — DWH & Integration (team lead)
featured: true
image: assets/img/acecook.jpg
imageAlt: FPT accompanies Acecook in building a modern management reporting system
link: https://fpt-is.com/fpt-dong-hanh-cung-acecook-xay-dung-he-thong-bao-cao-quan-tri-hien-dai/
linkLabel: Read the project announcement
summary: A ~100-table SQL Server warehouse holding 300 million records of sales-out data, fed by 80 SSIS ETL flows from SAP HANA, Oracle and Excel, with SSAS models serving Power BI.
tags: [Data Warehouse, SSIS, ETL, SQL Server, SSAS, Power BI, SAP HANA, Oracle]
highlights:
  - Surveyed, designed and implemented a Data Warehouse for Acecook Vietnam integrating SAP HANA, Oracle and Excel sources into MS SQL Server.
  - Built 80 SSIS ETL pipelines orchestrated with SQL Server Agent jobs; ~100 tables, ~300 million records.
  - Designed and deployed sales-out data models using SSAS as governed sources for Power BI reporting and analytics.
  - Led a team of four across the design and delivery.
---

## Context

Acecook Vietnam is the country's largest instant-noodle manufacturer. Their sales-out data — what actually moved from distributors to retail — lived in three different places: SAP HANA, an Oracle system, and a substantial number of Excel files maintained by regional teams. Every management report was somebody reconciling those three by hand.

The goal was a single warehouse those reports could stand on.

## The build

**Survey first.** Before any modelling, we catalogued every source: what it contained, who owned it, how often it changed, and how much of it could be trusted. The Excel files were the interesting part — they encoded business rules that existed nowhere else, and those rules had to be reverse-engineered before they could be automated.

**The warehouse.** Roughly 100 tables on MS SQL Server, about 300 million records. Layered: staging that mirrors source, a cleansed layer where the rules live, and a presentation layer modelled dimensionally for analysis rather than for the shape of any source system.

**The pipelines.** 80 SSIS packages, scheduled by SQL Server Agent. Incremental where the source supported a watermark; full refresh where it did not. Each package logs row counts and duration, so a slow load is visible before it becomes a failed load.

**The semantic layer.** SSAS models over the presentation layer. This is what stops "sales-out" meaning three different numbers in three different Power BI reports — the measure is defined once, in the model.

## What I would do differently

**Build the reconciliation into the pipeline from day one.** We validated against source during UAT and found discrepancies late. Row-count and sum checks that run automatically after each load would have surfaced those in week two instead of month four.

**Push harder on source data ownership early.** The Excel files had no owner, which meant every question about a rule took days to answer. Naming an owner per source at kickoff is a five-minute conversation that saves weeks.

## Result

Management reporting moved from manual consolidation to a governed warehouse with Power BI on top. For me it was the project that turned "I am an ABAP developer who is learning data" into a second discipline I could lead a team in.

> **To expand:** the dimensional model, the incremental load pattern, and the SSAS measure design.
