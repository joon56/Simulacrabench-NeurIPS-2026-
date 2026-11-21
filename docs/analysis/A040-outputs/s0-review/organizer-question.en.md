# Draft only — not sent

To: team@simulacrabench.org

Subject: HSCC clarification: learning from visible TRAIN during hosted predict()

Dear HSCC organizers,

Could you clarify the rule for using complete visible TRAIN rows during the
time-limited hosted execution of predict()?

The official website permits training on visible rows before prediction:
https://simulacrabench.org/

The starter-kit README says training must happen offline and that there is no
runtime training hook:
https://github.com/SituatedEvals/public/blob/main/README.md

For a submission with no runtime network access and no access to scored DEV/TEST
answers, which of the following are permitted within the total compute budget?

1. Fitting a small neural predictor and optimizing a retrieval metric on visible
   TRAIN answers inside predict().
2. Using frozen, publicly available pretrained weights while fitting preprocessing
   and constructing labeled in-context examples from visible TRAIN rows.
3. Splitting only visible TRAIN rows for fitting, choosing a fixed-family mixture,
   and checking it on a separate TRAIN subset, then refitting on all visible TRAIN.

Does “offline” require all such learning to finish before submission, or can these
operations occur within the isolated hosted runtime? Please identify the applicable
rule or clarification, including any distinction between Development and Final.

Thank you,
Minjoon Yoo
Team Odyssey
