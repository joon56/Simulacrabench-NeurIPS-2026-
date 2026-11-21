# C2 - remove A040 orchestration
C1: full builder_fail crashed c0000005 after assertions; identical imports plus
SDK managed noop exited0. Hypothesis: A040 Context/launcher/cleanup state is
unnecessary; Endpoint build plus existing transport reproduces the crash.
One reduction: replace Context/launcher execution with Endpoint connect/app/build
and AppStop, keeping real SDK builder, guard, transport and managed loop.
c2-minimal uses minimal_build. Crash localizes below orchestration; exit0 keeps
orchestration/retention interaction implicated. No scientific/Sandbox stage.