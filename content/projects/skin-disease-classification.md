---
title: Deep Learning for Skin Disease Diagnosis
slug: skin-disease-classification
org: uit
client: University of Information Technology, VNU-HCM
period: 05/2024 – 11/2024
start: 2024-05
end: 2024-11
role: Researcher — undergraduate thesis
featured: true
image: assets/img/jihmsp.jpg
imageAlt: Journal of Information Hiding and Multimedia Signal Processing
link: https://bit.kuas.edu.tw/2025/vol16/N1/06.JIHMSP-241105.pdf
linkLabel: Read the published paper (PDF)
summary: A classification method based on concatenation features for diagnosing skin diseases from images — my undergraduate thesis, published in the Journal of Information Hiding and Multimedia Signal Processing in 2025.
tags: [Deep Learning, Image Classification, Research, Python, Publication]
highlights:
  - Developed a classification method based on concatenation features for skin disease diagnosis from medical images.
  - Published in the Journal of Information Hiding and Multimedia Signal Processing (JIHMSP), Vol. 16 No. 1, 2025.
  - Co-authored with MSc. Duong Phi Long and Eng. Pham Nguyen Thanh Binh.
---

## The problem

Skin disease diagnosis from images is a hard classification problem for reasons that have little to do with model architecture. Classes look alike. Image quality varies enormously. Public datasets are imbalanced, with common conditions represented thousands of times and rare ones a handful. A model that reports high accuracy on such a dataset may simply have learned to predict the majority class.

## The approach

The method is built on **concatenation features** — rather than relying on a single feature representation, features from multiple extractions are concatenated into a combined representation before classification.

The intuition: different extractors are sensitive to different things. One responds to texture, another to colour distribution, another to shape and boundary. Skin conditions differ along all three axes, and none alone separates the classes cleanly. Concatenating gives the classifier a richer space to draw a boundary in.

## What research taught me that engineering did not

**Measure the thing you actually care about.** Accuracy on an imbalanced medical dataset is close to meaningless. Choosing the right evaluation metric was a longer argument than choosing the model.

**Baselines before ideas.** You cannot claim an improvement without something to improve on. Establishing a fair baseline is unglamorous and non-negotiable.

**Negative results are results.** Several combinations did not help. Knowing precisely which ones — and being able to say why — is a real part of the contribution.

**Write for reproduction.** A paper is only useful if someone else can rebuild the method from it. That standard of precision changed how I write technical documents at work.

## Publication

> Tran Van Quang, Duong Phi Long, Pham Nguyen Thanh Binh. *A Classification Method based on Concatenation Features for Diagnosing Skin Diseases.* Journal of Information Hiding and Multimedia Signal Processing, Vol. 16, No. 1, 2025.

This is the piece of work furthest from my day job, and I keep it here on purpose. The habits it built — measure, don't assume; establish a baseline; write it down precisely — are the ones I use most when a production system misbehaves.
