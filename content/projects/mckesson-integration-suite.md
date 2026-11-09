---
title: SimpleMDG Implementation for McKesson — SAP Integration Suite
slug: mckesson-integration-suite
org: laidon
client: McKesson
period: 05/2026 – Present
start: 2026-06
end:
role: SAP Technical Consultant
featured: true
current: true
image:
summary: Integration design for a US healthcare distributor — flows between SAP S/4HANA, SimpleMDG on BTP and surrounding systems, including an IDoc material inbound with 75 automated checks deployed error-free, and Event Mesh event handling.
tags: [SAP Integration Suite, Event Mesh, IDoc, SAP BTP, Master Data Governance, Business Partner, Product]
highlights:
  - Designed integration flows on SAP Integration Suite between SAP S/4HANA, SimpleMDG on SAP BTP, McKesson's customers and surrounding systems, including Event Mesh-based event handling.
  - Built an IDoc → SimpleMDG material inbound iFlow with 75 automated checks and a standard error passthrough, deployed error-free.
  - Implemented and customised key master data object types — Business Partner and Product — on the SimpleMDG platform.
---

## Context

McKesson is one of the largest healthcare distributors in the United States. In that industry, master data is not an administrative concern — a wrong product record is a clinical and regulatory problem, not a reporting inconvenience.

My scope is the integration layer: how master data moves between **SAP S/4HANA**, **SimpleMDG on SAP BTP**, McKesson's own customers, and the systems around them.

## The 75 checks

The piece I am most pleased with is the **IDoc → SimpleMDG material inbound iFlow**. Material master records arrive as IDocs and have to land in the governance platform — but not unconditionally.

The flow runs **75 automated checks** before anything is accepted, with a **standard error passthrough** for what fails. It deployed error-free.

The design principle is simple and worth stating plainly: **reject bad master data at the door**. The alternative — accept everything, clean it up later — is how master data problems become permanent. Once a bad record is in the governance system, it propagates to every consumer before anyone notices, and the cleanup costs more than the original validation would have.

The error passthrough matters just as much as the checks. A flow that silently drops what it cannot process is worse than one that fails loudly, because nobody finds out until a downstream system is missing data.

## Event-driven handling

Parts of the landscape use **Event Mesh** rather than request/response. The distinction I apply: a synchronous call when the caller genuinely needs the answer before it can continue, events when something happened that others may care about.

Master data governance leans towards the second. A business partner being approved is an event — several systems want to know, none of them should block the approval.

## Object types

Alongside the flows, I implemented and customised the key object types on the SimpleMDG platform: **Business Partner** and **Product**. This is where the product's generic governance model meets one customer's actual data — which fields are governed, which are derived, what validation applies, and which of McKesson's existing conventions the model has to accommodate.

> **In progress.** I will expand this with the interface inventory and the check catalogue as the rollout completes.
