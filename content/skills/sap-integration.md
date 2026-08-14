---
title: SAP Integration
slug: sap-integration
category: Integration & Data
icon: ⇄
short: Integration
level: 85
years: 3
summary: Connecting SAP to everything else — OData and REST APIs, BAPI and RFC, SAP PI/PO, SAP Integration Suite and SAP CI-DS, across warehouse systems, sales applications, planning tools and data warehouses.
tags: [OData, REST API, BAPI, RFC, SAP PI/PO, SAP Integration Suite, SAP CI-DS, IDoc]
featured: true
---

## Where I use it

Integration turned out to be the thread running through nearly every project I have worked on:

| Project | Integration |
| --- | --- |
| Kim Tin Group | SAP ↔ warehouse management application via **PI/PO** |
| Vinphaco | **OData** services for external sales applications |
| LOF | SAP IBP ↔ S/4HANA ↔ DWH via **SAP CI-DS**, with **RFC** receivers |
| Acecook | SAP HANA and Oracle → SQL Server via **SSIS** |
| Laidon Group | SAP BTP ↔ SAP ERP via **SAP Integration Suite** |

## Choosing the mechanism

- **OData** — when an external application needs to read or write SAP data live, with a self-describing contract. My default for app integration.
- **BAPI / RFC** — when another system needs to invoke SAP business logic and get a proper result back, including error messages.
- **PI/PO** — when the landscape already runs it, and the requirement needs routing, mapping or protocol conversion between more than two parties.
- **SAP Integration Suite** — the cloud-era answer, and what I use now for BTP-to-ERP.
- **CI-DS** — bulk data movement between SAP systems and a warehouse, on a schedule.
- **IDoc** — where the standard message type already models the document and the partner speaks it.

## The lessons that were not in the spec

**Errors matter more than the happy path.** Any interface can be built to work when everything is available and well-formed. The design question is what happens at 2 a.m. when the target system is down and 4,000 records are queued. On Kim Tin we ended up building a monitoring table and a reprocessing report that appeared nowhere in the specification and became the most-used part of the interface.

**Idempotency is not optional.** Any flow that can be re-run must be safe to re-run. On LOF, the receiving RFC checks for an existing document keyed on the planning reference before creating anything — otherwise a re-run means duplicate purchase requisitions, which is a worse problem than the one you were solving.

**Master data before transactional data.** Always. A transaction that lands before its master data is a failure with a confusing error message.

**Design the contract for the consumer.** My first OData service at Vinphaco exposed SAP's data model faithfully, and the calling application had to make four requests and join the results itself. The second version exposed what the consumer needed, in one call. The technically faithful design was the wrong design.

**Agree the field mapping with humans, not documents.** Two systems rarely mean exactly the same thing by the same word. That gets resolved in conversation with the people who use both systems, not by matching column names.

> **To expand:** interface architecture diagrams, and the error-handling pattern in full.
