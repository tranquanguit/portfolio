---
title: Master Data Governance — Custom Business Objects & Integration Flows
slug: laidon-mdg-rap
org: laidon
client: Laidon Group
period: 05/2026 – Present
start: 2026-05
end:
role: SAP Technical Consultant
featured: true
current: true
image:
summary: Building custom RAP business objects for master data governance in S/4HANA, and the integration flows connecting SAP BTP with SAP ERP through the SAP Integration Suite.
tags: [RAP Model, ABAP Cloud, Master Data Governance, SAP BTP, SAP Integration Suite, CDS, OData V4]
highlights:
  - Design and develop custom Business Objects in SAP S/4HANA using the RAP model and ABAP OOP for master data governance requirements.
  - Build integration flows through the SAP Integration Suite, connecting SAP BTP and SAP ERP systems.
  - Apply clean-core principles — extensions built on released APIs and ABAP Cloud rather than modifications to standard objects.
---

## Context

My current work at Laidon Group, starting May 2026. The focus is master data governance: making the creation, review, approval and distribution of master data an explicit, auditable process rather than something that happens by convention.

## The technical shape

**RAP business objects.** Each governed object is modelled as a RAP business object — CDS data model, behaviour definition, behaviour implementation, projection view, service definition and binding. The behaviour definition is where the governance rules live: which fields can change in which state, what validations must pass, and which determinations fire on save.

**Integration Suite.** The iFlows that move approved master data out to consuming systems, and bring change requests in.

**BTP ↔ ERP connectivity.** Destinations, communication arrangements and principal propagation — the plumbing that lets an extension running on BTP act on ERP data as the right user, with the right authorizations.

## Why RAP rather than classic ABAP

For a governance process specifically, RAP earns its complexity. The framework gives you draft handling, optimistic locking, a state model, and a consistent transactional contract — all things you would otherwise hand-write badly. And because the object is exposed as an OData V4 service by construction, the Fiori UI and any system integration consume the *same* definition of what is valid.

> **In progress.** This engagement is ongoing — I will publish specific stories here as milestones complete.
