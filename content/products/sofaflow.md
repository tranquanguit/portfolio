---
title: SofaFlow — Customer Lifecycle & Document Automation
slug: sofaflow
category: ERP & Business Systems
icon: ◫
status: private
period: 2026
start: 2026-03
role: Designer & developer
stack: Flask · PostgreSQL · SQLAlchemy · docxtpl
summary: A multi-tenant SaaS that runs the full customer lifecycle for sofa repair and manufacturing businesses — quotation to contract to handover to payment — and generates every Vietnamese document along the way.
tags: [Flask, PostgreSQL, SQLAlchemy, Multi-Tenant, DOCX Automation, RBAC, Bootstrap]
illustration: docflow
repo:
featured: true
audience: Sofa repair and manufacturing workshops, their sales staff and owners

problemHeading: The problem
problemLede: Sofa repair and manufacturing is a trade business — skilled work, real margins, and administration that runs almost entirely on paper.
problem:
  - The same details, typed four times :: Quotation, contract, handover note and payment record all repeat the customer, the measurements and the price. Every retyping is a chance to get one of them wrong.
  - Nobody knows where an order stands :: Was the contract signed? Has it been handed over? Has the customer paid the balance? The answer lives in someone's memory or a notebook.
  - Every workshop has its own paperwork :: Its letterhead, its terms, its way of itemising. Generic software forces them to abandon documents their customers already recognise.
  - Several stores, one owner :: Each store runs its own jobs, but the owner needs to see all of them without the stores seeing each other.

flowHeading: One record, four documents
flow:
  - Take the order :: Customer, store, measurements, items and price entered once.
  - Quotation :: Generated from the order into the workshop's own template.
  - Contract :: The same data, the customer's signature, no retyping.
  - Production and handover :: The handover note is generated when the work is delivered.
  - Payment :: Deposit and balance tracked against the order, not in a separate book.
  - Timeline :: Every stage visible on one screen, for every order.

capabilitiesHeading: What it does
capabilities:
  - Documents in your own format :: Each company uploads its own DOCX templates with variables. The output is the paperwork the business already uses, filled in correctly.
  - Visual order timeline :: Quotation to contract to handover to final payment, with the current stage obvious at a glance.
  - Multi-store under one company :: Stores run independently; the company sees across all of them.
  - Roles that match the shop :: Company admin, store admin and staff, each seeing what their job needs.
  - Bilingual interface :: Vietnamese for the shop floor, English where it helps, switchable on every page.
  - Complete tenant isolation :: One company's data is never visible to another.
highlights:
  - Multi-tenant architecture with complete data isolation between companies, and multi-store support within each company.
  - Order lifecycle tracked on a visual timeline from quotation through contract, handover and final payment.
  - DOCX document generation from per-company templates, so each business keeps its own paperwork.
  - Role-based access across company admin, store admin and user, with a bilingual Vietnamese/English interface throughout.
---

## Why this exists

Sofa repair and manufacturing is a trade business. The work is skilled, the margins are real, and the administration is almost entirely paper: a quotation written by hand, a contract typed in Word, a handover note, then chasing the final payment.

Every one of those documents repeats the same customer and order details. Every re-typing is a chance to get a price or a measurement wrong, and nobody finds out until the customer is standing in front of the finished sofa.

SofaFlow replaces that with one record that flows through the whole lifecycle.

## The shape of the system

**One order, four documents.** Quotation → contract → handover → payment. The order is entered once; each document is generated from it. The data cannot drift between documents because there is only one source of it.

**Templates belong to the company.** This was the design decision that made the product viable. Every business has its own paperwork — its letterhead, its terms, its way of itemising. Rather than forcing one layout, each company uploads its own **DOCX templates** with variables, and the engine substitutes the order's data into them. The output is the document they already use, filled in correctly.

**Multi-tenant from the first table.** Companies are isolated from each other, and a company can run several stores. Retrofitting tenancy into a system that assumed one customer is painful; building it in from the schema up costs little.

**Bilingual, because the users are.** Vietnamese for the shop floor, English where it helps. A language switcher on every page rather than two versions of the app.

## Architecture

A deliberately boring, layered Flask application — roughly 9,000 lines of Python across 35 ORM models:

| Layer | Responsibility |
| --- | --- |
| `models` | SQLAlchemy ORM — the data |
| `repositories` | Data access, isolated from business rules |
| `services` | Business logic — what the application actually decides |
| `routes` | HTTP endpoints only, thin by design |
| `utils/template_engine` | DOCX variable substitution |

Boring is the point. A trade business does not need a novel architecture; it needs something that still makes sense when someone has to change it in two years.

Deployment is containerised — Docker Compose with Nginx and Gunicorn, with a separate production compose file, a deployment guide and an operational runbook.

## What I would tell myself at the start

**The document templates were the product.** I thought the lifecycle tracking was the core and document generation was a feature. It was the other way round — the thing that made people willing to change how they work was getting their own paperwork out of it automatically.

> **To expand:** the template variable schema, and how the lifecycle state machine is modelled.
