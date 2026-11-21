# E060 first-run harness failure, before corrected execution

The first source suite stopped with ValueError before scoring any candidate:
the vector validator incorrectly unpacked official cells as pairs. Official
score.py:230 constructs triples (position, respondent ID, item). The completed
UNICEF predict call's returned vectors were not saved before that assertion.
No candidate score, selection result or release verdict was observed.

Preserve source.log, source-runtime.json, preflight.json and original registration;
the exact failed harness is archived as check_e060-attempt1.py.txt. This attempt
remains STOP_TECHNICAL. Recorded wall46.5746736s, peak tree RSS1034473472 and
commitment1095700480 bytes. Source control path completed one base pipeline;
normal source accounting implies3 neural requests, but the failed attempt did
not persist counters: mark that count inferred, not measured.

Root cause is the validator's tuple shape, not the candidate or scorer. Correct
only pair-to-triple unpacking. Freeze corrected harness under a separate
technical-retry1 output/local directory; do not overwrite the failed attempt.
Original model, assembly, data, splits, fitting loss and all decision thresholds
remain unchanged. Include failed46.5746736s in the original2700s total budget;
deadline unchanged. No successful suite is repeated: first suite never passed.

One corrected technical execution is within the user's request to perform work
toward a package. This is a documented technical retry of an unscored candidate,
not a statistical rescue. Existing historical study STOPs remain. A further
unexplained data/model failure stops for diagnosis without parameter search.
