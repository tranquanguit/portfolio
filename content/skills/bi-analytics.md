---
title: BI & Analytics
slug: bi-analytics
category: Integration & Data
icon: ◧
short: BI
level: 70
years: 1.5
summary: Semantic modelling and reporting on top of the warehouse — SSAS models serving Power BI, SAP Analytics Cloud, and Microsoft Fabric.
tags: [SSAS, Power BI, SAP Analytics Cloud, MS Fabric, Semantic Modelling, DAX]
---

## Where I use it

SSAS models over the Acecook warehouse feeding Power BI, and SAP Analytics Cloud — the subject of my C_SAC certification in April 2026.

## The point of a semantic layer

Without one, every report author writes their own version of every measure. Three Power BI reports quote three different figures for sales-out, all defensible, all built from the same warehouse, and leadership loses trust in the entire platform.

A semantic model fixes the definition in one place. Report authors compose from measures that already mean something rather than reinventing them. It is a governance mechanism far more than a technical one.

## What I have learned about reports

**Ask what decision it supports.** "A sales report" is not a requirement. "Which SKUs are underperforming in which regions this month, so we can act on them next week" is — and the two produce very different reports.

**Fewer numbers, better chosen.** A dashboard with forty tiles gets scanned and forgotten. Six that matter get used.

**Performance is a modelling problem.** A slow Power BI report is nearly always a model problem — the wrong grain, missing aggregations, or a relationship the engine cannot use efficiently — not a visualisation problem.

**Agree the definition before you build.** The written definition of "sales-out", signed off before a table was created, prevented more rework at Acecook than any technical decision on that project.

> **To expand:** SAC vs. Power BI in an SAP landscape, and notes on measure design.
