# E027 — concentrated-row evidence as net input, over E025
parent: E025
status: adopted
date: 2026-09-10

## Hypothesis

E024 (evidence block as net input for ALL rows) lost ~0.001 skill per
instrument on duplicate-free data because the block is a noise feature
there. Restricting the block to rows whose top candidate holds max
posterior weight ≥ CONC_SPLIT (the same bucket E019/E022 trust with
high λ) — zeros elsewhere — removes that harm while keeping the one
thing the mixture layer cannot express: cross-item household structure
(a co-respondent's answer to item A informing item B; household-level
items shared across members). Stacked on E025's 128×2 selection and
E022's mixture layer.

## Domain check

Pre-registered 2026-09-10 BEFORE implementation. (a) rows without a
concentrated match feed zeros — the net's extra columns are inert for
them; the inner early-stopping split bounds overfitting on the rest;
the λ layer recalibrates on the new base. (b) household-level items
(housing, HLP, assistance, income adequacy) are shared facts; a
learned map can exploit them, a per-item copy mixture cannot. (c) the
household sim has no cross-item structure — local checks are NO-HARM:
clean runner within ±0.002 of E025 and household sim > E025 − 0.005;
runtime CPU-side + one evidence pass (~+40 s local). Leaderboard is
the experiment: unhcr 0.90 ⇒ cross-item structure real (Grand 0.64);
0.89 ⇒ none exploitable, close the evidence-input idea; ≤0.88 ⇒ harm,
pin E025.

## Change

`src/models/ev_conc.py`: household_evidence_block with rows below
CONC_SPLIT zeroed; link_sharp.predict(layer_fn=hh_sharp_layer,
extra_fn=..., configs=E025's).

## Result

Household sim (ρ ∈ [0.2, 0.8]): E025 −0.5627 → E027 −0.5615, **+0.0011**
(no harm; no cross-item structure to gain from). Clean sandbox:
0.4436 / 0.5008 / 0.4534 / 0.5623 vs E025 0.4436 / 0.5006 / 0.4548 /
0.5629 — 3-inst −0.0006, every instrument within the ±0.002 bound (the
architecture change alone re-seeds the net; E024's uniform −0.001×3
harm is gone on unicef, residual on wb). Runtime ~330 s local CPU;
CPU-side ≈ E025 + one evidence pass; training on the H100.

## Decision

**Adopted as a pre-registered A/B** (no-harm conditions met; upside is
real-data cross-item household structure the sim cannot model).
Submission `submissions/2026-09-11-E027/`; readings in SCORES.md.
