# A005 — Sandbox oracle: the ceiling of any GIVEN-only model

Date: 2026-09-16. Type: technical (methods). Tool: `src/eval/oracle.py`,
test `tests/test_oracle.py`.

## Question

After E026–E031 (all ≤ +0.0013 locally) and the probe map (E032–E034:
unhcr base model alone ≈ 0.79, evidence +0.10), can a base-model change
(a different model class for P(item | GIVEN)) still be validated on the
sandbox, or is the local harness exhausted for that axis?

## Method

`make_sandbox` draws every GIVEN and PREDICT item from base logits plus
a one-dimensional hidden trait times a random loading, gates applied
afterwards. Replaying the generator's random stream (`default_rng([seed,
STREAM_DATA])`, same draw order) recovers the parameters exactly — the
regenerated frame equals the stored parquet column for column on all
three sandboxes. The Bayes-optimal GIVEN-only predictor is then
P(item | GIVEN) = ∫ P(item | t) p(t | GIVEN) dt on a 361-point grid,
with gate chains handled row-wise: a visible (GIVEN) parent is
conditioned on its observed value, a hidden (PREDICT) parent contributes
P(parent ∈ observed_if | t), recursively; gated GIVEN items enter the
posterior as asked·P(v | t) (or 1 − asked for the sentinel).

Attempt log: v1 marginalised visible parents over the trait — oracle
BELOW E025 on unicef (0.358) and wb (0.410), impossible; per-item
comparison showed a uniform −0.32 nats on wb's `group`-gated tracer
items ⇒ the bug; v2 (row-wise asked) fixed it.

## Result (phase 1, seed 0, exact skill)

| | unicef | world_bank | unhcr | 3-inst mean |
|---|---|---|---|---|
| oracle (GIVEN-only Bayes) | 0.5014 | 0.4585 | 0.5655 | 0.5085 |
| E025 (base, evidence off on unhcr) | 0.5006 | 0.4548 | 0.5633 | 0.5062 |
| headroom | 0.0008 | 0.0037 | 0.0022 | **0.0024** |

## Conclusion

The E025 base (ladder + shared-trunk net) sits within 0.004 of the
Bayes ceiling on every sandbox; the total GIVEN-only headroom (+0.0024)
is below the +0.005 adoption threshold. **No base-model class change
can clear the local bar, by construction.** This retroactively explains
E015/E017/E026 (capacity: local 0, real +0.01) and rules the base-model
axis out of local validation entirely: base-model hypotheses are
leaderboard A/Bs only, with the E028 risk. The household sim remains
the one local channel with headroom — the evidence layer — and the
probe map says the evidence layer is worth +0.10 on real unhcr.

Domain check: the sandbox's one-dimensional trait is a weaker structure
than real respondents' (real GIVEN coupling was 3–5× the sandbox's on
every submission), so "near the sandbox ceiling" does not mean "near
the real ceiling" — it means the sandbox cannot tell.
