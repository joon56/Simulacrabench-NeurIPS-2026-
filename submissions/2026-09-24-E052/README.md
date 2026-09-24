# E052 - Fixed evidence after base-only gate routing

Phase1 exploratory candidate, submission #30. Parent E041 remains the incumbent
(.64/.52/.49/.92); this configuration is not adopted. No hosted result yet.

UNHCR only: keep E041 fitting, retrieval and original item/bucket lambdas. Route
gates with evidence-free parent beliefs; then mix the same own-item evidence
into each final answer. UNICEF/WB delegate exactly to E041/E025. No new learner,
selector, external weights or runtime download. ZIP contains main.py only.

Clean UNHCR delta+.000167291 versus E041; existing household simulation
-.001080278. Both optional selector oracle bounds fail, so none is fitted.
This intervention tests a distinct routing interaction; no .65 prediction or
positive transfer claim. See SCORES.md for preregistered readings and caveats.

Release verification PASS:34tests, ZIP checker, official all3, clean regression
against both baselines, and every source/archive vector. Natural active path
changes25,911 clean UNHCR vectors and matches the diagnostic endpoint exactly.
Official402.795s <900, local CPU2threads; hosted timing is not guaranteed.
Consult verification.json and
../../docs/analysis/E052-outputs/active-assembly-parity.json for exact records.
The agent does not upload to Codabench.

Rebuild with `.venv/Scripts/python.exe scripts/assemble_e052.py`; exact parent
and base hashes are asserted. Preserve this snapshot when reporting the result.
