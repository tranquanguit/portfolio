---
title: AI-Assisted Delivery
slug: ai-assisted-delivery
category: Working & Leading
icon: ⬢
short: AI Delivery
radar: true
level: 80
years: 1.5
summary: Running AI coding agents inside real SAP delivery — code generation, ADT REST deployment and Jira automation — behind human review gates and byte-level verification.
tags: [AI-assisted Development, Coding Agents, ADT REST, Verification, Jira Automation, SAP Generative AI]
featured: true
---

## Where I use it

In production delivery at Laidon Group: code generation for the SimpleMDG 2.0 RAP refactor, automated deployment through ADT REST, and Jira automation — one run created **105 sub-tasks with 0 errors**.

It is also now a certified competence: **SAP Certified Associate — SAP Generative AI Developer**, April 2026.

## The only idea that matters: the gate

An AI agent can generate 400 ABAP objects faster than I can read the list. That is either a large productivity gain or a large unreviewed change to a customer system, and which one it is depends entirely on what happens next.

For the SimpleMDG refactor, every agent handover is gated by a **Git ↔ live-system byte comparison**. What is in the repository and what is active in the system must match exactly. If they diverge, the handover stops and a human looks at it.

That check is the engineering. Without it, "the agent generated it" is a statement of hope.

## What agents are genuinely good at

**The same transformation, many times.** 411 objects following one pattern is the ideal case — mechanical, verifiable, and tedious enough that humans make mistakes on object 300.

**Scaffolding.** A CDS view, its behaviour definition, its projection and its service binding have a shape. Generating the shape and reviewing the content is faster than typing both.

**Structured bulk operations.** Creating 105 Jira sub-tasks from a plan is not interesting work for a person.

## What they are bad at, in my experience

**Deciding whether the work should be done at all.** An agent asked to implement a requirement implements it. It will not tell you the requirement is wrong, or that standard SAP already does this.

**Anything needing landscape context.** The agent does not know that this customer is still on 7.31, that this field is governed, or that this table is 40 million rows.

**Being wrong quietly.** Human mistakes usually look like mistakes. Generated code is uniformly confident, which makes errors genuinely harder to spot by reading. This is the main reason the verification step is mechanical rather than a code review.

## How I would describe the discipline

Treat the agent as a **fast, tireless junior who never says "I'm not sure"**. You would not let that person deploy to a customer system unreviewed. The workflow is the same: clear scope, bounded task, mechanical verification, human sign-off.

> **To expand:** the byte-comparison harness, and the prompt structure I use for ABAP object generation.
