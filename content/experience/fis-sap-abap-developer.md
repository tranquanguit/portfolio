---
title: SAP ABAP Developer
slug: fis-sap-abap-developer
org: fis
company: FPT Information System
period: 07/2023 – 04/2026
start: 2023-07
end: 2026-04
location: Ho Chi Minh City, Vietnam
summary: Nearly three years building custom development on SAP S/4HANA — roughly 60 reports and functions across seven modules, 10 enhancements, and integration work on ten client projects.
tags: [ABAP OO, ALV, Adobe Forms, BAPI, BAdI, CDS Views, AMDP, PI/PO, OData, Fiori]
highlights:
  - Designed and developed custom modules and reports in SAP S/4HANA using ABAP and OOP to meet complex business requirements.
  - Delivered approximately 60 custom reports and functions across MM, SD, FI, FM, WM, PP and QM; created 10 enhancements to adapt standard SAP logic to customer business processes.
  - Handled SAP integration via API/BAPI and PI/PO, performance optimization (AMDP, parallel processing, CDS views), and enhancements using BAdIs and Customer Exits.
  - Developed SAP Fiori applications using Web GUI, built applications on the RAP model, and designed a backend service using the CAP model.
  - Collaborated with cross-functional teams on 10 SAP projects over 2+ years — 5 as a core team member and 5 as a supporting resource.
---

## Where I started

I joined FPT IS in July 2023, straight out of my third year at university, on the ES HCM technical resource team. The first project — Kim Tin Group — started three weeks later, so the learning curve was the project.

## What three years produced

Roughly **60 custom reports and functions** and **10 enhancements**, spread across seven modules:

| Module | Typical work |
| --- | --- |
| MM / WM | Goods movement reports, warehouse operation detail, stock reconciliation |
| SD | Sales document reports, pricing-related output |
| FI / FM | Financial document reports, budget and fund management, ticket revenue detail |
| PP / QM | Production order reporting, inspection lot and quality result handling |

Ten projects in total — five as a core team member (Kim Tin, Vinphaco, HURC1 Metro, Goldilocks, LOF) and five in a supporting role.

## The technical arc

**Year one — write it correctly.** Classic reporting: ALV, selection screens, Adobe Forms, BDC. Learning where standard SAP already does the job and where a custom object is genuinely warranted.

**Year two — write it fast.** Reports that ran fine in a sandbox with 10,000 records fell over against production volumes. This is where CDS views, AMDP and parallel processing stopped being CV keywords and became daily tools. Pushing aggregation down to HANA instead of looping in the application layer is the single biggest lever I found.

**Year three — write it so it connects.** Integration became the majority of my work: OData services for external sales apps, PI/PO interfaces for warehouse systems, RFC functions receiving data from SAP CI-DS, and a backend service built on the CAP model.

## What I would tell a new ABAP developer

1. **Read the standard code first.** Most "we need a custom program" requests are a standard transaction nobody configured properly.
2. **The spec is not the requirement.** Sit with the key user for twenty minutes and the actual business problem usually turns out to be smaller and different.
3. **Performance is a design decision, not a fix.** You cannot optimize your way out of a loop that reads the database inside it.
4. **Write the technical spec as you build.** The one you write afterwards is always worse and always late.
