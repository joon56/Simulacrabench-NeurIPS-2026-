# A018 release notices and artifact scope

This session prepares a TEST predictor and a distinct fallback. It does not
upload to Codabench or publish the private repository. The method PDF is a
separate attachment. Each ZIP must contain root-level main.py; Markdown, audit
records, proxy data and method PDFs are outside the executable archive.

## Rights and third-party materials

- Team source: proposed MIT grant in LICENSE-MIT-PROPOSED.txt is explicitly
  non-effective pending owner choice. Scope is only the two frozen submission
  mains and their identical ZIP copies, not the whole repository. MIT would
  permit the agreement's non-commercial research reproduction; it also permits
  commercial reuse. No claim that the draft itself satisfies an effective
  award-stage source delivery is made. Clause 7 requires the method now and
  licensed source from top three at award stage. Do not deliver award-stage
  source until an effective compatible license is selected.
- SituatedEvals public starter kit: MIT, revision
  ee427a94f6cc6a0d9d653b6be68c835a032e7552. Its complete notice is preserved as
  LICENSE-starter-kit.txt beside both release sources and included in new ZIPs.
  This notice licenses kit-owned material only, not the team's entire predictor.
- UCI Adult: Barry Becker and Ronny Kohavi (1996), DOI 10.24432/C5XW20,
  https://archive.ics.uci.edu/dataset/2/adult, CC BY 4.0. Development recoded
  responses and used profile-constrained/split proxy tasks; attribution and
  modifications are disclosed. No rows or derived fitted artifacts shipped.
- US Census Bureau 2023 SIPP public-use file:
  https://www.census.gov/data/datasets/2023/demo/sipp/2023-data.html. A014/E055
  used an audited one-month person extract, grouped splits and hospital gates.
  Public-use processing/imputation and US population limit transfer. No SIPP
  data, identifiers, extracted rows or learned coefficients are redistributed.
- TabPFN V2 development: Prior-Labs/TabPFN-v2-clf revision
  f851f2a3c941544733b712d8c0f96dfae9b28862, original weight SHA256
  f65a35685aeef42e31b796d9bfa34e68d6fc780bc98e7bff7763802964cf435f.
  Prior Labs License 1.1 and attribution notices remain with historical E049;
  TabPFN package code is separately licensed. Neither final model imports
  TabPFN or incorporates its weights, predictions or fitted artifacts.
- Runtime Python dependencies retain their own licenses. Hosted-installed
  dependencies are not bundled or relicensed. There is no requirements.txt,
  models.txt, pretrained weight or runtime network request in either archive.

Verified primary sources (2026-09-25): competition public API (saved JSON),
starter-kit remote HEAD and local full MIT text, UCI dataset license, Prior
Labs weight-license page, Census official 2023 release, OSI MIT text.
https://www.codabench.org/api/competitions/17822/
https://github.com/SituatedEvals/public/blob/main/LICENSE
https://huggingface.co/Prior-Labs/TabPFN-v2-clf/blob/main/LICENSE.txt
https://opensource.org/license/mit

## Operational dates

TEST: 2026-11-01 00:00 UTC to 2026-11-14 00:00 UTC (09:00 KST).
Engineering changes stop 2026-11-12 00:00 UTC / 09:00 KST.
Preferred user upload by 2026-11-13 00:00 UTC / 09:00 KST.
Recheck the live agreement and kit before upload; no autonomous upload.

Fallback is chosen before spending the one TEST submission. If E041 violates
a known contract/resource gate before upload, use the separately validated
E025 with its own four-page method. No automatic cross-model switch is added
inside predict(). After a participant-side failure, do not submit E025 as an
assumed retry. Only documented organizer infrastructure failure invokes the
agreement's retry procedure, using organizer instructions.
