---
title: sapwm3d — Warehouse Visualisation Platform
slug: sapwm3d
category: SAP Platform & Visualisation
icon: ⬢
status: building
period: 2026 – Present
start: 2026-04
role: Designer & developer
stack: TypeScript monorepo · canonical warehouse model · 2.5D viewer
summary: A SaaS platform that turns warehouse data into a spatial cockpit — a block-based 2.5D model of the warehouse showing occupancy, overload, blocked bins and data mismatches, built on a canonical model that is not tied to SAP.
tags: [TypeScript, Monorepo, Warehouse, 2.5D Visualisation, SAP EWM, Multi-Tenant, Excel Import]
repo: https://github.com/tranquanguit/warehouse-3d-4erp
featured: true
current: true
audience: Warehouse supervisors, inventory controllers, operations managers

problemHeading: The problem
problemLede: Warehouse data lives in ERP systems, WMS tools, spreadsheets and custom APIs. All of it is accurate and almost none of it is spatial.
problem:
  - Tables cannot show a warehouse :: A supervisor asking "where is the capacity problem" gets bin codes and quantities, and has to hold the physical layout in their head.
  - Every customer's warehouse is different :: Structures, naming and data maturity vary so much that bespoke visualisations never get reused.
  - Data disagrees with itself :: Stock recorded in one place and absent in another, blocked bins that nobody flagged, unmapped records sitting outside the model.
  - SAP-only tools exclude most warehouses :: Plenty of operations run on spreadsheets and a WMS, not on a fully configured EWM.

flowHeading: Design once, then watch it run
flow:
  - Model the warehouse :: Configure the structure and lay out the blocks in design-time mode.
  - Map the data :: Define how incoming records map onto the canonical model.
  - Ingest :: Excel or API first; SAP, S/4HANA and EWM as planned integration paths.
  - Visualise :: Stock positions, occupancy and capacity shown on the layout.
  - Spot the problems :: Overload, blocked bins, unmapped data and mismatches surfaced rather than searched for.
  - Export the template :: Share or reuse a warehouse configuration.

capabilitiesHeading: What it does
capabilities:
  - Block-based 2.5D cockpit :: Fast to read and fast to render, with no camera to fight and no occlusion.
  - A canonical model, not an SAP model :: The core is independent of SAP structures, so customers at any level of data maturity can be served.
  - Configuration instead of a rewrite :: A new customer with a different warehouse is a configuration exercise.
  - Excel and API ingestion first :: Because that is honestly where most warehouse data lives.
  - Mismatch detection :: Where the data disagrees with itself is shown, not hidden.
  - Multi-tenant by design :: Built to serve several customers from one platform.
highlights:
  - Design-time mode for configuring warehouse structure, layout, render settings and mapping rules; run-time mode for visualising stock, capacity and discrepancies.
  - A canonical warehouse hierarchy independent of SAP-specific structures, so the same core serves customers at different levels of data maturity.
  - Excel and API ingestion first, with SAP, S/4HANA, EWM and BTP as planned integration paths rather than hard dependencies.
  - Monorepo with separate web and API apps over five shared packages — canonical model, import schemas, template schema, viewer contracts and UI tokens.
---

## The problem

Warehouse data lives in ERP systems, WMS tools, spreadsheets and custom APIs. All of it is accurate and almost none of it is *spatial*. A supervisor asking "where is the capacity problem" gets a table of bin codes and quantities, and has to hold the physical warehouse in their head to interpret it.

The information needed to answer the question is already there. It is just not in a shape a person can see.

## What it does

Two connected modes:

**Design-time.** Configure the warehouse structure, lay out the blocks, set render settings and define how incoming data maps onto the model. This is the part that makes it a product rather than a bespoke visualisation — a new customer with a different warehouse is a configuration exercise, not a rewrite.

**Run-time.** Show stock positions, occupancy, capacity breaches, blocked bins and mismatches on that layout. Where is it full, where is it empty, and where does the data disagree with itself.

## The design decision that matters

**The core is not SAP-bound.**

I work in SAP all day, and the obvious move would have been to build straight onto EWM structures — storage types, sections, bins, `/SCWM/LAGP`. It would have been faster to the first demo and it would have capped the product at customers who run EWM and run it properly.

Instead the core uses a **canonical warehouse hierarchy**, with SAP as one source that maps into it. Excel and API ingestion come first, because that is honestly where most customers' warehouse data lives. SAP, S/4HANA, EWM and BTP are planned integration and deployment paths, not prerequisites.

That makes the hard problem explicit — the mapping layer between whatever the customer has and the model the viewer understands — rather than hiding it inside an assumption that everyone's data is already clean.

## Structure

A TypeScript monorepo:

| | |
| --- | --- |
| `apps/web` | The viewer and configuration UI |
| `apps/api` | Backend services |
| `packages/canonical-model` | The warehouse hierarchy everything else agrees on |
| `packages/import-schemas` | Validated shapes for Excel and API ingestion |
| `packages/template-schema` | Exportable warehouse templates |
| `packages/viewer-contracts` | The contract between data and renderer |
| `packages/ui-tokens` | Design tokens |

Splitting `viewer-contracts` out early was deliberate: the renderer and the data pipeline evolve at different speeds, and a typed contract between them is what stops a change in one quietly breaking the other.

## Why 2.5D rather than 3D

A full 3D warehouse looks impressive in a demo and is worse to work in. Operations staff need to find a bin and read a status, and a block-based 2.5D view does that faster — no camera to fight, no occlusion, and it renders acceptably on the hardware actually present on a warehouse floor.

> **In progress.** I will add the canonical model schema and the mapping-rule design as they settle.
