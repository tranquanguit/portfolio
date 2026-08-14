---
title: Data Warehousing & ETL
slug: data-warehouse-etl
category: Integration & Data
icon: ▤
short: DWH / ETL
level: 80
years: 1.5
summary: Designing warehouses and the pipelines that fill them — a ~100-table, 300-million-record SQL Server warehouse, 80 SSIS flows and 15 SAP CI-DS flows.
tags: [Data Warehouse, Dimensional Modelling, SSIS, ETL/ELT, SQL Server, SAP CI-DS, MS Fabric]
featured: true
---

## Where I use it

Acecook Vietnam, mainly: roughly 100 tables and 300 million records on MS SQL Server, fed by 80 SSIS packages from SAP HANA, Oracle and Excel. Then LOF, where 15 SAP CI-DS flows connected SAP IBP, S/4HANA and the warehouse.

## How I structure a warehouse

Three layers, always:

**Staging** mirrors the source, untouched. No cleansing, no business rules. When you need to answer "did the source really send that", this is the layer that answers.

**Cleansed / integrated** is where the rules live — deduplication, type conformance, key resolution, the mapping between three systems' idea of the same customer.

**Presentation** is modelled dimensionally, for how people ask questions, not for how the source stores rows. Facts and conformed dimensions.

The temptation is always to skip a layer for speed. Do not. Every hour saved by loading straight into the presentation layer comes back as a day of debugging when the numbers do not reconcile and you cannot tell whether the source or your logic is wrong.

## Pipeline practice

**Incremental where you can, full where you must.** A watermark column, a change-tracking mechanism, or a reliable modified-date makes incremental loading possible. Where the source offers none — the Excel files at Acecook — full refresh is honest and safe.

**Log every run.** Row counts in and out, duration, start and end. A load that is gradually slowing down is visible weeks before it fails.

**Reconcile inside the pipeline.** This is my biggest lesson from Acecook. We validated against source during UAT and found discrepancies late. Automated row-count and sum checks running after each load would have surfaced them in week two.

**Idempotent by design.** Re-running yesterday's load must not double yesterday's numbers.

## On the sources

The hardest source at Acecook was not SAP HANA or Oracle. It was Excel. Those files encoded business rules that existed nowhere else and had no owner, which meant every question about a rule took days to answer.

Two things I now do at kickoff: **catalogue every source** with a named owner, and **reverse-engineer the spreadsheet rules into written form** before automating them. Naming an owner per source is a five-minute conversation that saves weeks.

> **To expand:** the Acecook dimensional model and the incremental load pattern.
