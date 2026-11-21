# C4 - remove suspended-coroutine observation
C3 definition exits0; C2 actual build crashes. Installed Image.build invokes
resolver; local transport additionally traverses live coroutine await chains.
Hypothesis: fixture's live-coroutine introspection/retention causes finalization
interaction. Single change: remove that observation only from ImageGetOrCreate
response; keep real build/mount/function and exact byte validations.
c4-no-observer uses reduced minimal_build. Exit0 would implicate observation;
same crash rejects this sufficient-removal hypothesis. No guard removed.