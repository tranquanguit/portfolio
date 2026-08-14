---
title: RAP Model & SAP Fiori
slug: rap-fiori
category: SAP Development
icon: ◉
short: RAP / Fiori
level: 80
years: 2
summary: Building applications on the ABAP RESTful Application Programming model — business objects, behaviour definitions and OData V4 services — plus Fiori and Web GUI front ends.
tags: [RAP, ABAP Cloud, CDS, Behaviour Definition, OData V4, Fiori Elements, CAP]
featured: true
---

## Where I use it

RAP is the centre of my current work at Laidon Group, building custom business objects for master data governance. Before that, I built RAP-based applications at FPT IS and designed one backend service on the CAP model.

## The RAP mental model

A RAP business object is four things stacked:

1. **The data model** — CDS views defining the entities and their relationships.
2. **The behaviour definition** — what can be done to them: create, update, delete, actions, validations, determinations, and the authorization and locking rules.
3. **The behaviour implementation** — the ABAP classes where that behaviour actually lives.
4. **The projection and service binding** — a consumption-shaped view of the object, exposed as an OData service.

The thing that took me longest to internalise: **the behaviour definition is the contract**. Anything you enforce there is enforced for every consumer — the Fiori app, an external system calling the OData service, another ABAP program using EML. Anything you enforce only in the UI is not enforced at all.

## Determinations vs. validations

A distinction worth getting right early:

- A **validation** checks and refuses. It never changes data.
- A **determination** derives and fills. It changes data as a consequence of a change.

Mixing them — a validation that quietly sets a field — produces behaviour that is very hard to reason about later.

## Managed or unmanaged

**Managed** when the object is yours and RAP can own persistence — much less code, and you get draft handling and locking for free. **Unmanaged** when the data already lives behind existing logic you must go through, typically an existing BAPI or a legacy table with its own rules. Most of my objects are managed; the unmanaged ones are unmanaged for a specific, documented reason.

## On Fiori

I have built Fiori Elements apps over RAP services and Web GUI reports surfaced through the launchpad. The Fiori Elements route is the right default: annotations in CDS drive the UI, so the metadata and the interface cannot drift apart. When the requirement genuinely exceeds what annotations express, that is when a freestyle app is justified — not before.

> **To expand:** a full worked RAP business object, and notes on draft handling.
