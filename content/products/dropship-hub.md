---
title: Dropship Hub — Multi-Tenant Dropshipping Platform
slug: dropship-hub
category: ERP & Business Systems
icon: ⬓
status: building
period: 2026 – Present
start: 2026-10
role: Designer & developer
stack: Flask · PostgreSQL · JWT · htmx · Docker
summary: A dropshipping operations platform with transaction-based inventory accounting, bill-of-materials explosion, an explicit order state machine and a documented REST API — built the way an ERP module is built, not the way a store admin panel is.
tags: [Flask, PostgreSQL, Multi-Tenant, Inventory, BOM, State Machine, REST API, JWT, Docker]
repo:
featured: true
current: true
highlights:
  - Multi-tenant SaaS with isolated data per company and role-based access across super admin, company admin, warehouse manager and staff.
  - Transaction-based inventory — stock is derived from an immutable ledger rather than stored as a mutable number.
  - Bill of Materials with automatic explosion, so a bundled or assembled product consumes its components correctly.
  - Explicit order state machine: draft → confirmed → packed → shipped → delivered.
  - RESTful API with Swagger documentation, JWT authentication, and Alembic migrations.
---

## The ERP instinct, applied to a small business

Most dropshipping tools store stock as a number and update it. It works until two things happen at once, or until somebody asks *why* the number is what it is — and then there is no answer, because the history was overwritten.

Three years of SAP left me with a different instinct, and Dropship Hub is built on it.

## Inventory as a ledger, not a number

**Stock is never stored. It is derived.** Every movement is a transaction — receipt, issue, adjustment, transfer — and the quantity on hand is the sum of them. This is how accounting works, and it is how SAP's material documents work, for the same reason: you can always answer *how did we get here*.

The cost is a join and a sum where a naive design has a single column read. The benefit is that a stock discrepancy becomes a question with an answer instead of an argument.

## Bill of Materials

A BOM with **automatic explosion** — when a product that is assembled or bundled is ordered, its components are consumed in the right quantities. Straight out of the MM/PP playbook, and the piece that distinguishes a system that can handle kits from one that quietly goes wrong the first time somebody sells a bundle.

## The order state machine

**Draft → Confirmed → Packed → Shipped → Delivered.** Written as an explicit state machine rather than a status column that any part of the code can set.

The value is in what it forbids. A state machine makes invalid transitions impossible by construction, which means the rule lives in one place instead of being re-checked — and eventually forgotten — at every call site.

## Built as a platform

| Piece | Choice |
| --- | --- |
| API | REST, with Swagger documentation generated from the schemas |
| Auth | JWT, with role-based access across four roles |
| Schema changes | Alembic migrations, versioned |
| Transport | Jinja2 + Bootstrap + htmx — server-rendered, no SPA |
| Deployment | Docker Compose, separate dev and production stacks |

Roughly 18,000 lines of Python across 24 models, with a test suite and a seeding command for a working demo environment.

**On htmx rather than a SPA:** the application is forms and tables over a database. A React front end would have doubled the surface area to serve a UI that server-rendered HTML already handles well.

> **In progress.** This one is still being built — I will add the data model and the API contract as it stabilises.
