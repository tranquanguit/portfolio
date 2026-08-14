---
title: SAP S/4HANA Implementation — HURC1, HCMC Metro Line 1
slug: hurc1-metro-s4hana
org: fis
client: HURC1 — HCMC Metro Line No.1 Operating Company
period: 11/2024 – 06/2025
start: 2024-11
end: 2025-06
role: ABAP Developer (core team)
featured: true
image: assets/img/metro.jpg
imageAlt: FPT IS and HCMC Metro announce the IT system deployment plan
link: https://fpt-is.com/fpt-is-va-hcmc-metro-cong-bo-ke-hoach-trien-khai-he-thong-cntt-cho-van-phong-cong-ty-van-hanh-tuyen-metro-so-1/
linkLabel: Read the project announcement
summary: The IT backbone for the company operating Ho Chi Minh City's first metro line. I led development of FI sub-system reports and modules for financial document management and daily ticket-sales detail.
tags: [S/4HANA, FI, ALV, Public Sector, Reporting]
highlights:
  - Managed the development of new reports and modules for FI sub-systems covering financial document management.
  - Built daily detailed ticket-sales reporting for metro line operations.
---

## Context

Metro Line No.1 is the first urban rail line in Ho Chi Minh City — a project the city waited more than a decade for. HURC1 operates it, and FPT IS delivered the IT systems for the operating company. I worked on the finance side.

Working on this one felt different from a manufacturing rollout. The output is not a management report somebody reads at quarter end; it is the accounting record of a public transport system that the city rides every day.

## My scope

**Financial document management.** Reports and modules over FI documents — retrieval, drill-down, and the reconciliation views the finance team needed to close a period.

**Daily ticket-sales detail.** Ticket revenue arrives as a high volume of small transactions, and finance needed it broken out daily and in detail rather than as a monthly aggregate. This is a reporting problem where volume and granularity pull against each other: fine detail means many rows, and many rows means the report has to be built for performance from the first line of code.

## Design notes

- **Aggregate in the database, not in ABAP.** CDS views doing the grouping, with the report reading a result set that is already the right shape.
- **Selection screens that constrain by default.** A date range that defaults to today rather than an open-ended selection nobody meant to run.
- **One definition of revenue.** Agreed with finance up front and implemented once, so the daily report and the period report can never disagree.

## Result

The FI sub-system reporting went live with the operating company's systems. This was the project where I moved from taking a technical spec and building it to owning a functional area's development — clarifying requirements with the finance team directly, and being accountable for the delivery rather than just the code.

> **To expand:** the ticket-sales data model, and the performance approach in detail.
