# S3-PREP-A044 — disclosure and license inventory

Inventory/proposals only. No new license grant, publication or redistribution.
Current Terms unavailable; [rules audit](rules-and-schedule.md) distinguishes the
website summary from September clause7. The owner's source-license decision is
still required before any applicable source delivery; no whole-repository license.

| Material | Actual role in E041/E025 | License / action |
|---|---|---|
| Starter kit | Substantial kit-derived interface/helpers; both ZIPs contain the full notice | [MIT](https://github.com/SituatedEvals/public/blob/f980ef5059360fcf977ed7971af5c00ee5c1962f/LICENSE); retain copyright, permission and disclaimer. Current notice text compatible; existing notice hash recorded |
| Team predictor code | Two exact dated main.py files, no external fitted artifact | Owner choice pending. A018 MIT proposal is explicitly NOT EFFECTIVE |
| NumPy | Both direct runtime import | [BSD3 source license](https://github.com/numpy/numpy/blob/main/LICENSE.txt); retain notices if distributing source/binaries |
| pandas | Both direct runtime import | [BSD3](https://github.com/pandas-dev/pandas/blob/main/LICENSE); same notice/disclaimer/non-endorsement conditions |
| PyTorch | Both training/inference runtime | [BSD-style upstream license](https://github.com/pytorch/pytorch/blob/main/LICENSE), multiple copyright holders; bundled components can have additional notices |
| scikit-learn | Both OneHotEncoder runtime | [BSD3](https://github.com/scikit-learn/scikit-learn/blob/main/COPYING); preserve relevant license/notices |
| SciPy | E041 optimize/special direct import; indirect dependency of sklearn for both | [BSD3](https://github.com/scipy/scipy/blob/main/LICENSE.txt); binary libraries can have additional notices |
| threadpoolctl | E041 direct thread control; sklearn dependency | [BSD3](https://github.com/joblib/threadpoolctl/blob/master/LICENSE); not explicitly listed in hosted preinstall table, current image not verified |
| Python/re and stdlib | Interpreter, E041 regular expressions | Interpreter's own license; not shipped in ZIP. No claim that team MIT covers interpreter or dependency distributions |
| pyarrow/PyYAML and other harness packages | Organizer's data/config harness, not direct predictor imports | Existing kit requirements are not a predictor artifact manifest. No dependency binaries shipped here; any later environment redistribution needs version-specific transitive notice review |
| UCI Adult | Separate development proxies only | [CC BY4.0, Becker/Kohavi1996](https://archive.ics.uci.edu/dataset/2/adult). Credit source/license and describe recoding/profile-constrained splits; no rows/outputs/proxy fit in either ZIP |
| Census2023 SIPP | Separate observed proxy studies only | [Official public-use source](https://www.census.gov/data/datasets/2023/demo/sipp/2023-data.html); source/use documentation retained. No newly asserted blanket license or third-party rights clearance; no rows/outputs in ZIP |
| Prior Labs TabPFN V2 | Separate development experiments, including an earlier alternative | [Prior Labs License1.1](https://huggingface.co/Prior-Labs/TabPFN-v2-clf/blob/main/LICENSE.txt), Apache-derived with extra attribution §10. Not plain Apache/MIT; no weights/outputs/fitted proxy artifacts in E041/E025 |
| TabICLv2 | A040 separate fake-data adapter/runtime work; no E041/E025 integration | [A040 pinned evidence](../../A040-outputs/s1/source-register.md): code BSD3 at0dbff3e; weight metadata BSD3 at4dcd344. Metadata/code/weight evidence are distinct; no checkpoint opened now or license applied by this inventory |
| VAF/HOST documents and access-controlled microdata | A038/A039 metadata and header intake; linkage/asked-state HOLD, no empirical qualification | [Existing intake](../../A038-vaf-local-document-intake.md) and [header closeout](../../A039-outputs/s1/closeout.md). User reports approval/download, not unrestricted redistribution. No protected responses accessed in S3 and none included in either predictor |

Current upstream runtime license texts are saved as `license-*.txt` with fetch
hashes. They identify current upstream text, **not every installed wheel's license
bundle/version**. Both ZIPs contain only main.py and starter notice, no dependency
binaries, model weights or data. An award-stage source/environment package requires
its own exact component inventory; this audit does not give a legal guarantee.

TabPFN §10 adds a “Built with PriorLabs-TabPFN” display condition for covered
distribution and a model-name condition where its source/weights/outputs improve
a distributed model; its internal-testing exception is separately stated. Historical
TabPFN-containing releases remain under their own license obligations. The retained
E041/E025 byte lineage has no TabPFN code/weight/output integration; do not relicense
those historical alternatives or silently assert every prior distribution complied.
If a broader method-development derivative interpretation is asserted later, obtain
the applicable assessment before release. The actual use is disclosed regardless.

## Owner-review options — no choice made

Preferred simple option: scoped MIT for **only the team's original portions** of
`submissions/2026-09-25-E041/main.py` and/or `submissions/2026-09-25-E025/main.py`
and identical copies in the corresponding ZIP. Confirm actual copyright holders;
preserve starter and third-party notices. Exclude all data, weights, third-party
software, historical experiments and the rest of the repository. A018's existing
proposal can be reviewed; it is not activated or inserted into either ZIP here.

Alternative: an explicitly drafted research-reproduction grant restricted to the
same team-owned source, if the owner wants narrower rights. Exact wording must meet
the then-current competition Terms; a non-commercial summary is not itself a
license text. No agent signature, blanket repo LICENSE or inferred owner consent.

The four-page draft will disclose actual runtime fitting, method selection and
external development use. An access approval is not a license to publish VAF rows;
proxy evaluation is not permission to claim confidential TEST validation. Retired
second-account history stays disclosed, with no organizer waiver assumed.
