---
title: Dropship Hub — Warehouse Operations for Dropshipping
slug: dropship-hub
category: ERP & Business Systems
icon: ⬓
status: building
period: 2026 – Present
start: 2026-10
role: Product designer & developer
stack: React 19 · Fastify 5 · TypeScript · PostgreSQL
audience: Dropship warehouses, their agency partners, and the finance team behind both
summary: Warehouse operations software for dropshipping. It reads carrier labels straight out of PDFs, explodes combos, drives scan-based packing, hands over to carriers and settles agency debt — one flow from label to money, with a portal the agencies run themselves.
tags: [TypeScript, Fastify, React, PostgreSQL, Multi-Tenant, Metadata-Driven, Workflow Engine, Inventory]
repo:
featured: true
current: true

problemHeading: The problem
problemLede: A dropship warehouse handles hundreds of labels a day from dozens of agencies. When that runs on chat groups, spreadsheets and paper, the failures are always in the same six places.
problem:
  - Labels arrive in chat :: Every marketplace and every carrier prints a different label. Staff open each file and retype the tracking number and the contents by hand.
  - Every agency names things differently :: The same combo has a different name at every shop. The warehouse guesses, so components go missing or the wrong one goes in.
  - Cancelled orders still get packed :: The buyer cancels after the label is printed. Nobody finds out in time, the parcel ships, and the fee is paid twice.
  - Handover is counted by hand :: Nobody knows which parcel belonged to which agency or which request. Reconciling with the carrier takes the rest of the evening.
  - Debt lives in a notebook :: Goods, service fees, returns and discounts worked out by hand per agency. Month-end reconciliation runs for days.
  - Everyone can see the prices :: Warehouse staff need to know what goes in the box. They should not also see each agency's selling price, fees and discounts.

flowHeading: One flow, from carrier label to settled debt
flow:
  - Upload label PDFs :: On the portal, one file or many, labels from different marketplaces mixed together.
  - Read the labels, raise a request :: Tracking number, carrier and parcel contents are extracted. Duplicate tracking numbers are blocked.
  - Review and confirm :: Sales checks it, the agency confirms. Stock is reserved at that moment.
  - Print, stick, scan :: Print every label for the request in parcel order. Scanning the tracking number closes that parcel.
  - Hand over to the carrier :: One handover note can cover many requests. Signing it issues the goods and raises the debit note.
  - Settle :: Statements per agency, debt ageing, receipts. Returns are scanned back into stock.

capabilitiesHeading: What it does
capabilities:
  - Reads PDF labels without a template :: Text is read directly from the PDF — no photographs, no retyping. Shopee (SPX), Lazada, TikTok Shop, Viettel Post and SuperShip are preconfigured; anything else is read by the generic method.
  - Learns a label once :: Drag a box around the field on a sample label. The read area anchors to the nearest printed caption, so a label with an extra line still reads correctly.
  - Learns how each agency talks :: Declare the phrases an agency uses and they can paste "30 combo A, 20 B" into the form and get the right items out.
  - Explodes combos correctly :: Combos hold no stock of their own; how many sets can be built is derived from the scarcest component. The warehouse sees exactly what goes in the parcel.
  - Catches cancellations at the scanner :: An order cancelled on the marketplace raises a red warning when scanned, and the parcel is not counted as packed.
  - Stock that matches the floor :: Nobody edits a quantity. Every change goes through a document and leaves a trace — purchase, handover, transfer, return, stock count.
  - Separates money from goods :: "See prices" is its own permission. Money disappears everywhere — lists, detail, filters, Excel exports, dashboards, notifications — for anyone without it.
  - Nightly statements, per agency :: Each agency gets its own debt report at a time the company chooses, on the portal and by email or Zalo, with a QR code carrying the amount and reference.
  - Promotions instead of PDFs in a chat group :: Publish a channel price list with gifts; agencies opt in, and the gift attaches itself to the right parcel and ships with the goods.
  - One thread per agency :: Every exchange in one place, with read receipts and an owner, instead of dozens of chat groups.

highlights:
  - Reads carrier labels directly from PDF text with per-agency parsing rules, blocking duplicate tracking numbers across files, requests and agencies.
  - Scan-driven packing with partial progress ("packed 4/10", "delivered 0/10") and per-parcel state, so partial handover is a first-class case.
  - Append-only stock ledger with on-hand, reserved and available quantities, row-level locking for concurrent scanning, and a data integrity checker.
  - Metadata-driven platform — DocType definitions generate API validation, list queries, form UI, Excel templates and OpenAPI, so customer-specific fields are configuration.
---

## Who it is for

A dropship warehouse packing and shipping on behalf of many agencies — and the agencies themselves, who get their own portal rather than a chat group.

## The design idea

**Everything hangs off one request.** The labels, the parcels, the goods issued, the confirmation messages and the resulting documents all live inside the packing request. There is no second place to look.

That is what makes the rest possible: progress can be partial and still be accurate ("packed 4/10, delivered 2/10"), every screen can show the same **next action** so whoever opens the request knows who is being waited on, and the debit note at the end is built from what was actually handed over rather than what was ordered.

## Architecture

| Piece | Choice |
| --- | --- |
| Front end | React 19 + Ant Design, one shell serving both the company app and the agency portal |
| API | Node 24 + Fastify 5, TypeScript run directly with no build step |
| Metadata | DocType definitions drive API validation, list queries, form UI, Excel templates and OpenAPI |
| Engine | Shared CRUD, a workflow engine defined in the database, numbering, settings, audit and an outbox |
| Label reading | PDF text extraction with per-agency parsing rules, plus generation and page splitting |
| Integration | ERP connectors as plugins, carrier and marketplace connectors, outbox → webhook with HMAC |

**The metadata layer is the point.** Entity definitions live in the database rather than in code, so the API contract, the list filters, the form layout and the Excel import template are all generated from one definition. A customer-specific field is configuration, not a release.

**Stock is a ledger, not a number.** On-hand, reserved and available are derived from documents. Reserved is taken the moment the agency confirms. Rows are locked when written, so several people scanning at once still produce the right number. There is an integrity checker that can be run at any time: stock equals the ledger, reserved equals open orders, no negative stock, debt equals the debt ledger.

## Isolation and safety

Each company's and each agency's data is separated **in the database**, not by a filter the application remembers to apply. Buyer details are kept private, every action is logged, and closed accounting periods cannot be edited.

> **In progress.** v2 is a full rewrite; the original Flask application is kept in `legacy/` for reference only. I will add the DocType model and the integration contract as they settle.
