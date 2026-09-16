"""Bayes-optimal GIVEN-only predictor on the kit sandbox.

The sandbox draws every GIVEN and PREDICT item from base logits plus a
one-dimensional hidden trait times a random loading (make_sandbox).
Replaying the generator's random stream recovers those parameters, so
P(item | GIVEN) can be computed exactly by marginalising the trait on a
grid (gate chains handled recursively: items are independent given the
trait). The resulting skill is the ceiling of ANY model that sees only
the GIVEN block — the local headroom for base-model changes.

usage: python src/eval/oracle.py [unicef|world_bank|unhcr] [seed]
"""
import sys; sys.path.insert(0, "C:/Users/USER/Desktop/SimulacraBench")
import numpy as np, pandas as pd
from src.eval.runner import ensure_sandbox, load_config, KIT, load_frames, sample_rows, floored, grade
import make_sandbox as ms

def oracle(name, seed=0, grid_points=361):
    """Return the kit grader's result dict for the Bayes-optimal
    GIVEN-only predictor on the named sandbox (phase 1)."""
    config = load_config(str(KIT / "config.yml")); settings = config["sandbox"]
    schema, d = ensure_sandbox(name, config)
    frame, cells, truth = sample_rows(schema, load_frames(str(d), schema), 1)

    # --- replay the generator's random stream to recover base logits and loadings
    n = schema["dataset"]["n_rows"]
    rng = np.random.default_rng([seed, ms.STREAM_DATA])
    items = ms.generated_items(schema)
    trait = rng.normal(size=n)
    params = {}
    for nm in ms._generation_order(schema, items):
        options = list(schema["items"][nm]["values"]); width = len(options)
        base = np.log(rng.dirichlet(np.full(width, settings["dirichlet_alpha"])) + 1e-12)
        load = rng.normal(scale=settings["trait_scale"], size=width)
        rng.random((n, 1))
        params[nm] = (options, base, load)

    # sanity: regenerated frame must equal the sandbox (check one GIVEN column's marginal)
    records = schema["items"]
    given = [k for k in items if records[k]["class"] == "GIVEN"]
    predict = [k for k in items if records[k]["class"] == "PREDICT"]

    grid = np.linspace(-4.5, 4.5, grid_points); prior = np.exp(-0.5 * grid**2); prior /= prior.sum()
    def probs(nm):  # [grid, width]
        options, base, load = params[nm]
        lg = base[None, :] + grid[:, None] * load[None, :]
        w = np.exp(lg - lg.max(1, keepdims=True)); return w / w.sum(1, keepdims=True)
    P = {nm: probs(nm) for nm in params}

    # asked-probability per grid point, ROW-WISE: a visible (GIVEN) parent is
    # conditioned on its observed value (indicator), a hidden (PREDICT) parent
    # contributes P(parent in observed_if | trait); chains recurse.
    held_rows = sorted({r for r, _, _ in cells})
    gval = schema["gated_value"]
    given_idx = {g: j for j, g in enumerate(given)}
    vals = frame[given].to_numpy(dtype=object)
    _cache = {}
    def asked_row(nm, r):
        key = (nm, r)
        if key in _cache:
            return _cache[key]
        g = records[nm].get("gate")
        if not g:
            out = np.ones(len(grid))
        else:
            par = g["parent"]
            if par in given_idx:
                v = vals[r, given_idx[par]]
                out = (np.ones(len(grid)) if v in g["observed_if"]
                       else np.zeros(len(grid)))
            else:
                opts_p = params[par][0]
                idx = [opts_p.index(o) for o in g["observed_if"] if o in opts_p]
                out = asked_row(par, r) * P[par][:, idx].sum(1)
        _cache[key] = out
        return out

    # posterior over the trait from the row's GIVEN block (gated GIVEN items
    # contribute asked * P(v | trait), or 1 - asked when they hold the sentinel)
    post = {}
    for r in held_rows:
        lp = np.log(prior)
        for j, gname in enumerate(given):
            options = params[gname][0]; v = vals[r, j]
            a = asked_row(gname, r)
            if v == gval:
                lp += np.log(1.0 - a + 1e-300)
            elif v in options:
                lp += np.log(a * P[gname][:, options.index(v)] + 1e-300)
        w = np.exp(lp - lp.max()); post[r] = w / w.sum()

    vectors = []
    for r, _, item in cells:
        options = params[item][0]; q = post[r]
        if records[item].get("gate"):
            pa = asked_row(item, r)
            vec = np.append((q[:, None] * pa[:, None] * P[item]).sum(0), (q * (1 - pa)).sum())
        else:
            vec = (q[:, None] * P[item]).sum(0)
        vectors.append(vec)
    res = grade(schema, config, floored(vectors, schema, cells, config["scoring"]["floor"]), truth, cells)
    return res


if __name__ == "__main__":
    name = sys.argv[1] if len(sys.argv) > 1 else "unhcr"
    seed = int(sys.argv[2]) if len(sys.argv) > 2 else 0
    res = oracle(name, seed)
    print(f"{name}: oracle GIVEN-only skill {res['skill']:.4f} on {res['n_cells']} phase-1 cells")
