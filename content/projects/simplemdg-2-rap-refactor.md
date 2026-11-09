---
title: SimpleMDG 2.0 — Platform Refactor to RAP
slug: simplemdg-2-rap-refactor
logo: simplemdg
org: laidon
client: Laidon Group (product)
period: 05/2026 – Present
start: 2026-05
end:
role: SAP Technical Consultant
featured: true
current: true
image:
summary: Refactoring the core of Laidon's master data governance product onto RAP for S/4HANA 2023 — 105 ABAP packages measured, a 411-object shared core rebuilt, and a 70-entity-set Business Partner OData API, deployed through an automated ADT REST pipeline.
tags: [RAP Model, ABAP Cloud, CDS Views, OData V4, ADT REST, AI-assisted Development, Refactoring]
highlights:
  - Refactored the core of Laidon's master data governance product from a measured baseline of 105 ABAP packages.
  - Rebuilt the shared core (411 objects) and the Business Partner OData API (70 entity sets, 126 CDS views) through an automated ADT REST deploy-and-activate pipeline.
  - Ran AI coding agents behind human review gates, with every handover verified by a Git ↔ live-system byte comparison.
---

## Context

SimpleMDG works. That is the hard part of a refactor like this — nobody is asking you to fix something broken. The product governs master data for customers in the US and Europe, and it does so on a codebase that grew the way successful products grow: by solving the next problem.

The goal of 2.0 is to put the core on **RAP for S/4HANA 2023**, so that the next five years of features are cheaper to build than the last five.

## Measure before you move

The first deliverable was not code, it was a number: **105 ABAP packages**. Before touching anything, I built an inventory of what actually existed — packages, objects, dependencies, what was reachable and what had quietly died.

This matters more than it sounds. A refactor without a baseline has no definition of done, and no way to prove you did not lose anything. Every claim below is measured against that inventory.

## What got rebuilt

| Piece | Scale |
| --- | --- |
| Shared core | 411 objects |
| Business Partner OData API | 70 entity sets, 126 CDS views |

The Business Partner API is the interesting one. Business Partner is the most-integrated object in any SAP landscape — it is what every surrounding system wants to read and write. 70 entity sets is not over-engineering; it is the real shape of what a BP means once you include addresses, roles, bank data, relationships, identifications and the governance state around all of it.

126 CDS views to serve it is also where the performance work lives. A view graph that wide is exactly where **CDS fan-out** happens — rows multiplying through joins long before the result set is cut back. Designing it so that does *not* happen was most of the thinking.

## The deployment pipeline

Moving 411 objects by hand is not realistic, and SAP's transport tooling is built for changes, not for rebuilds. So the handover runs through an **automated ADT REST deploy-and-activate pipeline**: objects are pushed to the system over ADT's REST interface and activated programmatically.

## Where AI fits, and where it does not

I ran **AI coding agents** for a significant share of the mechanical transformation — the same object pattern applied hundreds of times is exactly what they are good at.

![Every handover gated by a Git ↔ live-system byte comparison.](diagram:ai-gate)

But a code generator producing 411 objects is only useful if you can prove what landed. So every handover is gated by a **Git ↔ live-system byte comparison**: what is in the repository and what is active in the system must match exactly, byte for byte. If they diverge, the handover stops.

That check is the whole design. Without it, "the agent generated it" is a statement of hope. With it, the agent is a fast typist and the verification is the engineering.

> **In progress.** This refactor is ongoing — I will add the measured before/after on the full object set as it completes.
