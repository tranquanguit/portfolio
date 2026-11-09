---
title: Reject Bad Master Data at the Door
slug: master-data-at-the-door
topic: SAP & ERP
date: 2026
status: draft
publishedOn: This site
summary: Why the cheapest place to stop a bad material master is the inbound interface, and what 75 automated checks on an IDoc flow actually buy you.
tags: [Master Data Governance, SAP Integration Suite, IDoc, Data Quality, MDG]
featured: true
---

## The rule

**A master data record should be rejected at the interface, not cleaned up afterwards.**

It sounds obvious written down. In practice almost every landscape I have worked in does the opposite: accept what arrives, let it flow, and fix the problems when somebody downstream complains.

## Why "fix it later" loses

Master data is not transactional data. A wrong sales order affects one sale. A wrong material master affects every document that references it, in every system it has been distributed to, for as long as the record exists.

By the time somebody notices, the bad record has:

- been replicated to the systems subscribing to it,
- been referenced by transactional documents that are now inconsistent,
- and been copied into reports that nobody will re-run.

Cleaning that up is not "correcting a record". It is an archaeology project with a business impact attached.

## What this looks like in practice

On the McKesson implementation, material master records arrive as IDocs and land in SimpleMDG on SAP BTP. The inbound iFlow runs **75 automated checks** before anything is accepted, with a standard error passthrough for what fails.

![The inbound interface is the cheapest place to stop a bad record.](diagram:integration-landscape)

Seventy-five sounds like a lot until you enumerate what can actually be wrong with a material master: missing mandatory fields for the plant it is being extended to, units of measure that do not convert, classification values outside the allowed set, references to org units that do not exist in the target, and so on. Each check is small. The set of them is what makes the difference.

## The part people get wrong: the error path

A validating interface that silently drops what it cannot process is **worse** than one with no validation, because the sender believes the data arrived.

The error passthrough matters as much as the checks:

1. The rejected record is visible, with the reason.
2. The sender finds out.
3. Someone can correct and resend without a developer being involved.

If any of those three is missing, the validation will be switched off within a month — because from the outside it will look like the interface is losing data.

## The counter-argument, and my answer

The objection is always the same: *strict validation blocks the business*.

It does, sometimes. That is the point. The question is not whether the record gets blocked; it is **where** it gets blocked — at an interface, where one person fixes one record, or three months later across six systems.

What makes strictness acceptable is the feedback loop. Reject fast, say exactly why, and make resubmission cheap.

> **Draft.** This is a first pass — I plan to expand it with the check taxonomy and worked examples.
