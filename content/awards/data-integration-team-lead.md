---
title: Leader & Mentor — Data Integration Team
slug: data-integration-team-lead
type: achievement
icon: 👥
issuer: FPT IS
org: fis
date: 2025 – 2026
period: 2025 – 2026
featured: true
summary: Led a team of four across data integration and warehousing projects — defining goals and KPIs, delivering on time, and building the team's capability in a domain none of us had shipped before.
tags: [Leadership, Mentoring, Data Engineering, KPIs]
---

## The situation

In early 2025 the department won data warehousing work in a field it had not staffed for. Four of us were assigned to it. None of us had delivered a warehouse before, and the delivery date was not negotiable.

I was asked to lead.

## How I ran it

**Definitions before code.** We agreed in writing what "sales-out" meant before anyone created a table. That single document prevented more rework than any technical decision on the project — because every disagreement that would otherwise have surfaced at UAT surfaced in week one instead, when it was cheap.

**KPIs the team could see.** Flows completed, load duration, reconciliation variance against source. Numbers on a board that everyone could read. People correct their own course when they can see where they are; status meetings mostly tell the lead what they already suspect.

**Rotate the hard problems.** Whoever had not yet touched CI-DS took the next CI-DS flow, paired with someone who had. Two weeks slower up front, considerably faster for the rest of the project, and — the real point — no single point of failure when someone took leave.

**Unblock, then step back.** Most of what I did day to day was remove whatever was stopping someone, and then not hover over the result.

## What I got wrong

**I under-invested in automated data quality checks.** We validated against source during UAT and found discrepancies late, which cost us a tense fortnight. Reconciliation belongs in the pipeline, running after every load, not in a phase at the end. This is the first thing I would change.

**I let source ownership stay ambiguous.** Several Excel sources had no named owner, so every question about a business rule took days to route. Naming an owner per source at kickoff is a five-minute conversation.

## What I learned about leading

That the technical part is the easy part. Four capable people with a clear definition of done will solve the technical problems. The lead's actual job is making sure the definition of done is right, that nobody is stuck, and that the team ends the project more capable than it started.

> **To expand:** the KPI framework in detail.
