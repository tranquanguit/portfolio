---
title: ABAP & ABAP OO
slug: abap-oo
category: SAP Development
icon: ◈
short: ABAP OO
level: 90
years: 3
summary: Custom development in SAP S/4HANA using ABAP and object-oriented design — roughly 60 reports and functions delivered across seven modules.
tags: [ABAP, ABAP OO, ALV, Classes & Interfaces, Exception Handling, Unit Testing]
featured: true
---

## Where I use it

Everything starts here. Around 60 custom reports and functions across MM, SD, FI, FM, WM, PP and QM, on five implementation projects and one maintenance engagement.

## How I write ABAP

**Objects, not includes.** Classic ABAP reports grow into thousand-line includes that only their author can navigate. A local class per responsibility — one for selection, one for the data read, one for the business rules, one for output — stays readable and, more importantly, stays testable.

**Separate reading from deciding from displaying.** The single most useful structural rule I know. When the database read is isolated in its own method, you can profile it. When the business rule is isolated, you can unit-test it without a database at all.

**Exceptions over return codes.** `RAISE EXCEPTION TYPE` with a proper exception class carries context that `sy-subrc = 4` never will.

## Things I had to learn the hard way

**`SELECT` inside a `LOOP` is the default performance bug.** It passes every test on a development system with a hundred rows and collapses on production volumes. Read the set once, sort it, and use a hashed or sorted table to look up inside the loop.

**`FOR ALL ENTRIES` needs a guard.** If the driver table is empty, the statement reads everything. Check it first, every time.

**Field symbols instead of work-area copies** when looping over large internal tables — `ASSIGNING <fs>` avoids copying each row.

**Do not swallow errors.** A `TRY / CATCH` with an empty `CATCH` block is a bug you will find at 2 a.m. six months later.

## What I would tell someone starting

Read standard SAP code. Not to copy it — some of it is thirty years old — but because you will discover that most requirements for a custom program are actually a standard transaction that was never configured. The best custom object is often the one you talk the client out of.

> **To expand:** worked examples — an ALV report structured as classes, and the internal-table patterns that matter at volume.
