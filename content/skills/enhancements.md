---
title: Enhancements & Extensibility
slug: enhancements
category: SAP Development
icon: ⊕
short: Enhancements
level: 85
years: 3
summary: Adapting standard SAP behaviour to customer processes with BAdIs, Customer Exits, enhancement points and BDC — around 10 enhancements delivered, and a strong preference for the least invasive option that works.
tags: [BAdI, Customer Exit, Enhancement Point, User Exit, BDC, Clean Core]
featured: true
---

## The judgement call

Every enhancement is a small permanent tax. It has to be retested at every upgrade, it makes standard behaviour surprising to the next consultant, and it is the first suspect when something breaks. So the real skill is not knowing the techniques — it is knowing whether the enhancement should exist at all.

My order of preference:

1. **Configuration.** Is this genuinely not configurable? Ask the functional consultant twice.
2. **A released extension point** — BAdI, enhancement spot. Supported, upgrade-safe, documented by SAP.
3. **Classic Customer Exit / User Exit.** Older mechanism, still widely present in the field.
4. **Modification.** Effectively never, and only with the client's explicit written agreement.

## What I use in practice

**BAdIs.** The default. Object-oriented, multiple implementations possible with filters, and cleanly separated from standard code. Around ten of my enhancements are BAdI implementations.

**Customer / User Exits.** On older functionality where no BAdI exists. Function-module or include based, with the usual caveat: the exit runs inside standard code, so what you can safely touch is limited and what you break can be far-reaching.

**Enhancement points.** Implicit and explicit. Useful, but I treat implicit enhancements with suspicion — they are easy to add and easy to forget.

**BDC.** Not an enhancement technique but adjacent: driving a standard transaction from code when no BAPI exists. Used on Goldilocks and LOF. It works, and it is fragile — it depends on screen sequence, which SAP can change in a support package. Always the fallback, never the first choice.

## Rules I hold to

- **Keep the logic outside.** The enhancement should call a class of yours, not contain 300 lines. Then it is testable, and it is portable if the extension point ever moves.
- **Fail safe.** An enhancement that throws an unhandled exception takes the standard transaction down with it.
- **Document why, not what.** The code shows what it does. The comment should record which requirement forced it and who signed off, because in three years that is the only question that matters.
- **Log it centrally.** Keep a register of every enhancement, where it sits and why. Upgrade testing becomes a checklist instead of an archaeology project.

## Where clean core changes this

ABAP Cloud narrows the options deliberately: released APIs and released extension points only. Coming from three years of on-premise work where implicit enhancements were always available, the constraint felt restrictive at first. It is not — it is the same discipline I was already arguing for, enforced by the compiler instead of by code review.

> **To expand:** a decision tree, and a real BAdI implementation walkthrough.
