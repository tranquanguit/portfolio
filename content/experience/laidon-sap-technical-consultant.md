---
title: SAP Technical Consultant
slug: laidon-sap-technical-consultant
org: laidon
company: Laidon Group
period: 05/2026 – Present
start: 2026-05
end:
location: Ho Chi Minh City, Vietnam
current: true
summary: ABAP/RAP backend and SAP Integration Suite flows for SimpleMDG, Laidon's master data governance product on SAP BTP — across 10 US and EU customer implementations, with OData response times cut by up to 94%.
tags: [RAP Model, ABAP Cloud, SAP Integration Suite, SAP BTP, Master Data Governance, Event Mesh, Performance]
highlights:
  - Deliver the ABAP/RAP backend and integrations for SimpleMDG across 10 customer implementations for US and EU clients; owned 220+ Jira tickets, 92% closed or in customer testing.
  - Built SAP Integration Suite iFlows — an IDoc → SimpleMDG material inbound with 75 automated checks deployed error-free, MuleSoft–Salesforce customer interfaces, and flat-file exports.
  - Cut OData response times by up to 94% (Product read 27 s → 4.4 s, BP $expand 43 s → 2.5 s) and traced production dumps and timeouts to RAP paging and CDS fan-out root causes.
  - Prepared customer rollouts — transport packages, Basis setup guides, a 36-object downport from ABAP 7.40 to 7.31, and CUA for 19 clients across 7 systems.
  - Ran AI coding agents behind human review gates for code generation, ADT REST deployment and Jira automation (105 sub-tasks in one run, 0 errors).
---

## The move

After nearly three years at FPT IS delivering S/4HANA projects on-premise, I moved to Laidon Group in May 2026 — from project work for one customer at a time to **product** work shipped to many.

SimpleMDG is Laidon's master data governance product, built on SAP BTP. I own the ABAP/RAP backend and the integration layer, and the same code lands in ten different customer landscapes across the US and Europe.

## What changes when it is a product

**Ten landscapes, one codebase.** A fix is not "a fix for this client" — it has to hold in every system the product runs in. That changed how I write: fewer assumptions about configuration, far more defensive reading of master data, and no shortcuts that happen to work because of how one customer happened to set things up.

**Customer rollout is part of engineering.** Transport packages, Basis setup guides, CUA across 19 clients and 7 systems, and a 36-object downport from ABAP 7.40 to 7.31 for a customer still on the older stack. None of that is glamorous. All of it decides whether the product actually reaches production.

**Tickets as the unit of work.** 220+ Jira tickets so far, 92% closed or sitting in customer testing.

## Performance became the headline

The biggest single contribution has been latency. Two numbers I keep coming back to:

| Call | Before | After |
| --- | --- | --- |
| Product read | 27 s | 4.4 s |
| Business Partner `$expand` | 43 s | 2.5 s |

Both were traced to the same family of causes: **RAP paging behaving differently than expected under load, and CDS fan-out** — a view graph that multiplies rows long before the result set is cut back down. Production dumps and timeouts that had been written off as "the system is slow" turned out to have specific, fixable root causes.

The lesson I keep relearning: performance problems are rarely in the code you wrote last. They are in the shape of the data model underneath it.

## Integration

**SAP Integration Suite** is where most of my non-ABAP time goes. The piece I am most pleased with is an **IDoc → SimpleMDG material inbound iFlow with 75 automated checks**, deployed error-free — the checks catch bad master data at the door rather than letting it land and be cleaned up later.

Alongside that: **MuleSoft–Salesforce** customer interfaces, flat-file exports, and **Event Mesh**-based event handling.

## AI agents, behind a gate

I run AI coding agents for code generation, ADT REST deployment and Jira automation — one run created 105 sub-tasks with 0 errors.

The part that matters is not the agent, it is the **gate**. Every handover is verified by a Git ↔ live-system byte comparison, and nothing reaches a customer system without human review. Agents are fast and confidently wrong in ways that are hard to spot by reading; the verification step is what makes the speed usable rather than dangerous.
