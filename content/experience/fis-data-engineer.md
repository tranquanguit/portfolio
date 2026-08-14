---
title: Data Engineer
slug: fis-data-engineer
org: fis
company: FPT Information System
period: 03/2025 – 04/2026
start: 2025-03
end: 2026-04
location: Ho Chi Minh City, Vietnam
summary: Led a four-person data integration team — a ~100-table warehouse holding 300 million records, 80 SSIS ETL flows, and 15 SAP CI-DS flows connecting IBP, S/4HANA and the warehouse.
tags: [Data Warehouse, SSIS, ETL, SAP CI-DS, SSAS, Power BI, SQL Server, MS Fabric]
highlights:
  - Designed and implemented a Data Warehouse for Acecook Vietnam with approximately 100 tables and 300 million records.
  - Developed 80 SSIS ETL flows ingesting data from SAP, Oracle and Excel sources.
  - Built 15 SAP CI-DS data flows integrating SAP IBP, SAP S/4HANA and the Data Warehouse.
  - Led a team of four — defining goals and KPIs, ensuring on-time delivery, and growing the team through knowledge sharing and hands-on problem solving.
---

## A second discipline, on purpose

In early 2025 the department won data warehousing work in a field it had not staffed for. I volunteered to be the one who learned it, alongside my ABAP work — partly because the ABAP side had started to feel comfortable, and mostly because I kept running into the same wall from the other direction: I would build a report inside SAP, and the business would then ask for it joined against data that lived in Oracle or a spreadsheet.

## What I built

**The warehouse.** Around 100 tables and 300 million records on MS SQL Server for Acecook Vietnam, covering sales-out data. Staging, cleansing and presentation layers, with the dimensional models designed for BI consumption rather than mirroring source schemas.

**The pipelines.** 80 SSIS ETL flows pulling from SAP HANA, Oracle and Excel, orchestrated by SQL Server Agent jobs. Incremental loads where the source allowed watermarking, full refresh where it did not.

**The SAP integration.** 15 SAP CI-DS data flows tying SAP IBP, SAP S/4HANA and the warehouse together — five transactional flows and ten master data flows.

**The semantic layer.** SSAS models over the warehouse so Power BI reports read from one governed definition of a measure instead of each report inventing its own.

## Leading the team

This was my first time leading rather than contributing. Four people, a new domain for all of us, and a delivery date.

What worked:

- **Written definitions before written code.** We agreed what "sales-out" meant, in one document, before anyone built a table. That document prevented more rework than any technical decision.
- **KPIs the team could see.** Flows completed, load duration, reconciliation variance against source. Visible numbers, not status meetings.
- **Rotating the hard problems.** Whoever had not yet touched CI-DS took the next CI-DS flow, with a pair. Slower for a fortnight, much faster afterwards.

What I would do differently: I under-invested in automated data quality checks at the start and paid for it during UAT. Reconciliation should be part of the pipeline, not a phase.

## Why the combination matters

An ABAP developer who understands warehouses asks better questions about the source system. A data engineer who has actually written the extract inside SAP knows why that table has 40 million rows and which of its fields can be trusted. Doing both is the point.
