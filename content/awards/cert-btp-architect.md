---
title: SAP Certified Professional — Solution Architect, SAP BTP
slug: cert-btp-architect
type: certification
icon: 🏛
issuer: SAP
code: P_BTPA
date: 26 April 2026
period: April 2026
featured: true
summary: SAP's professional-level architecture certification for SAP Business Technology Platform — the one that moved me from "I build on BTP" to "I can design what gets built on BTP".
tags: [SAP Certification, SAP BTP, Solution Architecture, Integration, Extensibility]
---

## What it covers

P_BTPA is a **professional**-level exam rather than associate-level, and the difference is real: it asks what you would choose and why, not what a service is called.

- **Architecture and design** on SAP BTP — which extension pattern fits which problem.
- **Integration architecture** — Integration Suite, Event Mesh, API Management, and when each belongs.
- **Extensibility** — side-by-side on BTP versus in-stack with ABAP Cloud, and the trade-off between them.
- **Security and identity** — IAS, destinations, principal propagation.
- **Operations** — multitenancy, subaccounts, transport and lifecycle.

## Why this one mattered most

The other three certifications confirm things I do. This one changed what I am asked to do.

Working on SimpleMDG, the questions that reach me are increasingly not "how do I implement this" but "should this live in the ERP core or on BTP", "does this integration need Event Mesh or will a synchronous call do", "what happens to this design at ten customers instead of one". Those are architecture questions, and before this I was answering them from intuition built on a handful of projects.

Studying for P_BTPA gave me the vocabulary and — more useful — the **catalogue of options**. The most common failure in a design review is not choosing badly, it is not knowing an option existed.

## The one idea I use most

**Clean core is an architectural position, not a coding rule.** It is easy to say "don't modify standard". It is harder to answer the follow-up: *then where does this logic go?* The BTP architecture model gives a real answer — side-by-side when the logic has its own lifecycle, in-stack ABAP Cloud when it genuinely belongs to the business object, and integration in between.

> **To expand:** a worked example of the side-by-side vs. in-stack decision on a real requirement.
