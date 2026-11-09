---
title: ShopMind — Multimodal Search & Glass-Box RAG
slug: shopmind
category: AI & Search
icon: ◉
status: live
period: 2026
start: 2026-10
role: Designer & developer
stack: FastAPI · Elasticsearch · React · SigLIP2 · PostgreSQL
summary: A shopping assistant you can see inside — text, image and composed search over 1,500 products, a RAG assistant whose every citation is verified, and a glass-box inspector that shows exactly why each result came back.
tags: [RAG, Elasticsearch, FastAPI, React, SigLIP2, Multimodal Search, Evaluation, PostgreSQL]
repo: https://github.com/kt1101/shopmind-rag
featured: true
audience: Anyone evaluating RAG for a product catalogue — and researchers who want the numbers

problemHeading: The problem with most RAG demos
problemLede: Getting a model to answer from your documents takes an afternoon. Getting it to answer correctly, cite evidence you can verify, and refuse when it cannot, is the actual engineering.
problem:
  - Citations nobody checks :: An answer appears with references attached, and there is no way to tell whether they support the claim or were merely nearby in the retrieved text.
  - They never say "I don't know" :: Asked something the corpus cannot answer, the system answers anyway — which in a shopping context means inventing a return policy.
  - You cannot see why :: When a result is wrong, there is no trace showing which step produced it, so debugging is guesswork.
  - "We improved retrieval" is a feeling :: Without seeded, reproducible benchmarks, no change can be shown to be an improvement.

flowHeading: How a question becomes an answer
flow:
  - Understand the query :: Rewrite it to stand alone, detect intent, extract filters.
  - Retrieve :: BM25 and dense vectors over products, reviews and policies, fused with Reciprocal Rank Fusion.
  - Build the context :: Select candidates per source and assemble exactly what the model will see.
  - Generate :: Stream the answer with citations attached.
  - Validate :: Every cited ID must appear in the context actually sent, or it is rejected.
  - Trace :: Every step, score and timing recorded and shown in the inspector.

capabilitiesHeading: What it does
capabilities:
  - Composed search :: "Like this picture but in black" — an image anchors the shape, text modifies it. The closest thing to how people actually shop.
  - Verified citations :: A citation that cannot be traced to the evidence the model saw is rejected rather than rendered.
  - An explicit refusal path :: When evidence is insufficient the answer is `insufficient_evidence`, not a plausible invention.
  - Glass-box inspector :: Parsed query, BM25 / dense / RRF ranks, matched terms, latency waterfall, the raw query DSL, and the citation check.
  - Shopping plans with a budget :: Split the need, retrieve per need, optimise against a budget, and explain the result with citations.
  - Measured, not asserted :: Recall@10, nDCG@10 and MRR@10 at a fixed seed, with ablations, every run written to its own directory.
highlights:
  - Multimodal retrieval over 1,500 Amazon Berkeley Objects — text, image, and composed search ("like this picture but in black") using BM25 + dense kNN fused with RRF.
  - A RAG assistant answering from products, reviews and store policies, with every citation validated against the context actually sent to the model, and an explicit refusal when evidence is insufficient.
  - A glass-box inspector producing a pipeline trace for every request — each step, its input and output, scores, timings and reasoning.
  - Reproducible IR and RAG evaluation — Recall@10, nDCG@10, MRR@10 with fixed seeds, ablations, and every run written to its own directory.
---

## The idea

Two things bother me about most RAG demos.

**They cannot show their work.** An answer appears with citations attached, and there is no way to tell whether the citation supports the claim or was simply nearby in the retrieved text.

**They never say "I don't know".** Asked something the corpus cannot answer, they answer anyway.

ShopMind is a small, complete shopping product built to do the opposite of both.

## Search

Retrieval over a 1,500-product subset of Amazon Berkeley Objects, in three modes:

- **Text** — BM25 and dense vectors, fused with Reciprocal Rank Fusion.
- **Image** — SigLIP2 embeddings, find visually similar products.
- **Composed** — *"like this picture but in black"*. An image anchors the shape, text modifies it. This is the one that is genuinely hard, and the one closest to how people actually shop.

Elasticsearch 8.15 is the search store, holding both the lexical index and the dense vectors. A multilingual E5 embedder covers text-to-text; SigLIP2 covers image and cross-modal.

## Citations that are actually checked

The RAG assistant answers from three evidence sources — product data, Amazon reviews, and experimental store policies.

The rule it enforces: **a cited ID must appear in the context that was sent to the model.** Not "appears in the corpus" — appears in *this* request's context. A citation that cannot be traced to the evidence the model actually saw is rejected rather than rendered.

And when the evidence is not there, the answer is `insufficient_evidence`. Refusing is a feature. A shopping assistant that invents a return policy is worse than one that says it does not know.

## Glass-box

Every search and RAG request emits a **pipeline trace**: each step, its inputs and outputs, scores, timings and the reason for each decision.

The admin console exposes it — a Search Inspector showing the parsed query, BM25 / dense / RRF ranks, matched terms, a latency waterfall and the raw Elasticsearch DSL; a RAG Inspector showing candidates per source, the exact context sent, the prompt, and the citation check. Plus a 2D embedding map, a search playground, hot-reloadable config with rollback, and a policy CMS.

This is the part I would keep if I had to throw the rest away. Being able to answer *why did it return that* turns debugging a retrieval system from guesswork into reading.

## Measured, not asserted

An evaluation centre with seeded benchmarks — **Recall@10, nDCG@10, MRR@10** at seed 42 — plus ablations and a staged RAG roadmap. Every run is written to `runs/<timestamp>_<name>/`.

Without this, "we improved retrieval" is a feeling. With it, it is a number you can reproduce.

## Scale

Roughly 40,000 lines across a FastAPI backend and a React + Vite front end, with ~97 test files. The backend is layered — interfaces, application use cases, domain, infrastructure adapters — with a pipeline engine driven by YAML definitions, so a retrieval strategy is configuration rather than a code change.

> **To expand:** the RRF fusion parameters, and what the ablations actually showed.
