---
title: SAP S/4HANA Maintenance — Goldilocks Bakeshop, Inc.
slug: goldilocks-s4hana-maintenance
org: fis
client: Goldilocks Bakeshop, Inc. (Philippines)
period: 06/2025 – 04/2026
start: 2025-06
end: 2026-04
role: ABAP Developer (core team)
featured: true
image: assets/img/goldilocks.jpg
imageAlt: Goldilocks Bakeshop SAP S/4HANA maintenance project
link: https://www.facebook.com/photo/?fbid=1137587591719058&set=a.351614693649689
linkLabel: Project announcement
summary: My first international engagement — maintaining and extending S/4HANA for a Philippine retail chain, developing new FICO functionality, Web GUI reports for Fiori, and Adobe Forms.
tags: [S/4HANA, FI, CO, BAPI, BDC, Adobe Forms, Fiori, Web GUI, AMS]
highlights:
  - Participated in SAP S/4HANA maintenance for international customers in the Philippines, developing new FICO functionality by simulating SAP standard logic with BAPIs and BDC.
  - Authored technical specification (TS) documents for created and modified functionality.
  - Developed Web GUI reports for Fiori interfaces and Adobe Forms to customer requirements.
---

## Context

Goldilocks is a well-known bakeshop and restaurant chain in the Philippines. This was an application maintenance and support engagement rather than a greenfield implementation — a running production system, real users, and change requests arriving continuously.

It was also my first project with a client outside Vietnam, working across languages and time zones in English.

## How maintenance differs from implementation

An implementation has a go-live date and a blank slate. Maintenance has neither. Everything you build lands in a system that is already live, already integrated, and already trusted by people who will notice immediately if it behaves differently.

Practically, that changed three things about how I worked:

1. **Understand before you change.** Most of the effort went into reading the existing custom code and the configuration around it. The change itself was often small.
2. **Regression is the risk.** The question is never only "does my change work" but "what else touches this".
3. **Documentation is a deliverable, not an afterthought.** Which is why the TS documents mattered here more than on any implementation I had done.

## My scope

**New FICO functionality.** Extending finance and controlling with logic the standard system did not cover, implemented by driving standard behaviour through BAPIs where one existed, and BDC where none did.

**Web GUI reports for Fiori.** Surfacing classic reports through the Fiori launchpad, so users got one entry point rather than switching between SAP GUI and Fiori.

**Adobe Forms.** Customer-specific print output built to their layout requirements.

**Technical specifications.** Every object created or modified, documented — purpose, logic, objects touched, test cases. On an AMS engagement, the person maintaining your code next year may not be you.

## What working internationally taught me

Write it down, and write it plainly. When you cannot walk to someone's desk and there is a time-zone gap between question and answer, an ambiguous sentence costs a full day. My written English got noticeably more precise on this project, and my specs got better as a result.

> **To expand:** the FICO functions in detail, and the Adobe Form templates.
