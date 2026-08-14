---
title: SAP S/4HANA Integration — LOF
slug: lof-s4hana-integration
org: fis
client: LOF
period: 11/2025 – 12/2025
start: 2025-11
end: 2025-12
role: ABAP Developer — Integration (core team)
featured: true
image:
summary: Data integration between SAP IBP, SAP S/4HANA and the Data Warehouse using SAP CI-DS — five transactional and ten master data flows — with ABAP RFC functions creating planned orders and purchase requisitions on arrival.
tags: [S/4HANA, SAP IBP, SAP CI-DS, RFC, BDC, BAPI, Data Integration]
highlights:
  - Designed and implemented data integration flows between SAP IBP, SAP S/4HANA and the Data Warehouse using SAP CI-DS — five transactional data flows and ten master data flows.
  - Developed ABAP RFC functions to receive data from SAP CI-DS, perform transformation, and create planned orders and purchase requisitions using BDC and BAPI techniques.
---

## Context

A short, dense project. SAP Integrated Business Planning (IBP) produces the supply plan; S/4HANA executes it. Between them sits the question every planning integration has to answer: how does a number in a planning tool become a document in the execution system, reliably, every cycle?

## The architecture

Fifteen flows through **SAP Cloud Integration for Data Services (CI-DS)**:

- **Ten master data flows** — the reference data both systems must agree on. Master data first, always: a transactional flow that lands before its master data is a flow that fails.
- **Five transactional flows** — the planning results moving into execution.

On the S/4HANA side, **ABAP RFC functions** receive what CI-DS delivers, transform it into the shape SAP expects, and create the actual documents: **planned orders** and **purchase requisitions**, via BAPI where available and BDC where not.

## Design decisions worth recording

**Idempotency.** A planning cycle can be re-run. If a re-run creates duplicate purchase requisitions, the integration has caused a bigger problem than it solved. The receiving RFC checks for an existing document keyed on the planning reference before it creates anything.

**Fail loudly, in one place.** Errors surface in a single log the operations team can read, with enough context to identify which planning record failed and why — rather than being scattered across CI-DS run logs and SAP application logs.

**Transformation belongs on the ABAP side.** CI-DS moves data well. Business rules about what constitutes a valid planned order belong next to the system that enforces them, where they can be tested and where the next developer will look for them.

## Result

Fifteen flows delivered inside a two-month window, connecting planning, execution and reporting. This project is the direct bridge between my two disciplines — the data engineering work and the ABAP work turned out to be the same problem viewed from opposite ends.

> **To expand:** the CI-DS flow inventory, the idempotency check, and the error-log design.
